# type: ignore
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


"""Local directory resource for managing directory creation and cleanup."""

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, cast

from attrs import define, evolve

if TYPE_CHECKING:
    pyvider_local_directory = Literal["pyvider_local_directory"]

from provide.foundation import logger
from provide.foundation.errors import resilient

from pyvider.exceptions import ResourceError
from pyvider.hub import register_resource
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_num, a_str, a_unknown, s_resource

#: Whether this platform stores POSIX mode bits a `stat` can read back.
#:
#: Windows does not. CPython synthesises `st_mode` from the file attributes --
#: a writable directory is always `_S_IFDIR | 0o111 | 0o666` -- so
#: `st_mode & 0o777` is 0o777 whatever was chmod'ed. Reading `permissions` off
#: it there reports an observation the platform cannot make.
MODE_BITS_OBSERVABLE = sys.platform != "win32"


@define(frozen=True)
class LocalDirectoryConfig:
    path: str
    permissions: str | None = None


@define(frozen=True)
class LocalDirectoryState:
    path: str
    permissions: str | None = None
    id: str | None = None
    file_count: int | None = None


def _count_files(path: Path) -> int:
    """Files directly in `path`. Subdirectories are not files and are not counted."""
    return len([f for f in path.iterdir() if f.is_file()])


@register_resource("pyvider_local_directory")
class LocalDirectoryResource(
    BaseResource["pyvider_local_directory", LocalDirectoryState, LocalDirectoryConfig]
):
    config_class = LocalDirectoryConfig
    state_class = LocalDirectoryState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "path": a_str(required=True, description="The path of the directory to manage."),
                "permissions": a_str(
                    optional=True,
                    computed=True,
                    description="The permissions for the directory in octal format. Must start with '0o' (e.g., '0o755').",
                ),
                "id": a_str(computed=True, description="The absolute path of the directory."),
                "file_count": a_num(computed=True, description="The number of files in the directory."),
            }
        )

    @resilient()
    async def _validate_config(self, config: LocalDirectoryConfig) -> list[str]:
        if config.permissions:
            is_valid = config.permissions.startswith("0o") and all(
                c in "01234567" for c in config.permissions[2:]
            )
            if not is_valid:
                logger.debug(
                    "Invalid permissions format",
                    permissions=config.permissions,
                    expected_format="0o755",
                )
                return [
                    f"The value '{config.permissions}' is not a valid octal string. It must be prefixed with '0o', for example: '0o755'."
                ]
        logger.debug("Configuration validation passed", permissions=config.permissions)
        return []

    async def _create(
        self,
        ctx: ResourceContext[LocalDirectoryConfig, LocalDirectoryState, None],
        base_plan: dict[str, Any],
    ) -> tuple[dict[str, Any] | None, None]:
        config = cast(LocalDirectoryConfig, ctx.config)
        if not config:
            return None, None

        base_plan["permissions"] = config.permissions or "0o755"
        base_plan["id"] = str(Path(config.path).resolve())
        # Unknown, not 0. `mkdir(exist_ok=True)` may adopt a directory that
        # already holds files, and anything written into it between plan and
        # apply counts too, so the provider cannot know this until apply.
        # Promising a literal recorded a count that was never re-derived, and
        # Terraform warned about the mismatch on every later refresh.
        base_plan["file_count"] = a_unknown(a_num())

        return base_plan, None

    async def _update(
        self,
        ctx: ResourceContext[LocalDirectoryConfig, LocalDirectoryState, None],
        base_plan: dict[str, Any],
    ) -> tuple[dict[str, Any] | None, None]:
        config = cast(LocalDirectoryConfig, ctx.config)
        if not config:
            return None, None
        base_plan["permissions"] = config.permissions or "0o755"
        # Not planned unknown here, unlike _create. Doing so needs the
        # refinement check that shipped in pyvider 0.6.0; on 0.5.2, which this
        # package still supports, the apply is rejected. Leaving it alone the
        # update inherits the prior count, apply re-derives it, and both
        # versions accept that.
        return base_plan, None

    @resilient()
    async def _create_apply(
        self, ctx: ResourceContext[LocalDirectoryConfig, LocalDirectoryState, None]
    ) -> tuple[LocalDirectoryState | None, None]:
        planned_state = cast(LocalDirectoryState, ctx.planned_state)
        path = Path(planned_state.path)
        logger.debug("Creating directory", path=str(path))

        # Check if path exists as a file (not a directory)
        if path.exists() and not path.is_dir():
            raise ResourceError(
                f"Cannot create directory at '{path}': path exists as a file. "
                "Please remove the file or choose a different path."
            )

        path.mkdir(parents=True, exist_ok=True)
        try:
            permissions_str = planned_state.permissions or "0o755"
            path.chmod(int(permissions_str, 8))
            logger.debug(
                "Set directory permissions",
                path=str(path),
                permissions=planned_state.permissions,
            )
        except (ValueError, TypeError) as e:
            raise ResourceError(
                f"Invalid permissions format: {planned_state.permissions}. Must be an octal string like '0o755'."
            ) from e

        # Counted here rather than echoed from the plan, which promised unknown.
        # `read` counts the same way, so a refresh finds what apply recorded.
        return evolve(planned_state, file_count=_count_files(path)), None

    async def _update_apply(
        self, ctx: ResourceContext[LocalDirectoryConfig, LocalDirectoryState, None]
    ) -> tuple[LocalDirectoryState | None, None]:
        return await self._create_apply(ctx)

    @resilient()
    async def read(
        self, ctx: ResourceContext[LocalDirectoryConfig, LocalDirectoryState, None]
    ) -> LocalDirectoryState | None:
        if not ctx.state or not ctx.state.path:
            logger.debug("No state or path provided for read operation")
            return None
        configured_path = ctx.state.path
        path = Path(configured_path)
        if not path.is_dir():
            logger.debug("Path is not a directory or doesn't exist", path=str(path))
            return None
        # Where the mode is not observable the prior value stands: nothing on
        # disk contradicts it, and synthesising 0o777 instead makes Terraform
        # plan a change back to the configured value on every refresh, which
        # the next refresh undoes again.
        if MODE_BITS_OBSERVABLE:
            current_permissions = "0o" + oct(path.stat().st_mode & 0o777)[2:]
        else:
            current_permissions = ctx.state.permissions
        file_count = _count_files(path)
        logger.debug(
            "Read directory state",
            path=configured_path,
            permissions=current_permissions,
            file_count=file_count,
        )
        assert self.state_class is not None
        return self.state_class(
            # Echo the configured/prior path string verbatim. Round-tripping it
            # through Path() would normalise away things like a "./" prefix
            # (Path("./x") stringifies to "x"), which makes Terraform see
            # perpetual drift on every subsequent plan since the value read
            # back never matches what the practitioner wrote.
            path=configured_path,
            permissions=current_permissions,
            id=str(path.resolve()),
            file_count=file_count,
        )

    async def _delete_apply(
        self, ctx: ResourceContext[LocalDirectoryConfig, LocalDirectoryState, None]
    ) -> None:
        state = cast(LocalDirectoryState, ctx.state)
        if not state or not state.path:
            return
        path = Path(state.path)
        if path.is_dir():
            try:
                path.rmdir()
            except OSError:
                logger.warning(f"Directory {path} is not empty and will not be removed.")


# 🧩🔧🔚
