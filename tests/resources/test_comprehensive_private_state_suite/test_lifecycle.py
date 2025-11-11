    """Test complete resource lifecycle with private state"""

    @pytest.mark.usefixtures("provider_in_hub")
    @pytest.mark.asyncio
    async def test_complete_resource_lifecycle_with_private_state(
        self, encryption_key_env
    ):
        """Test full CRUD lifecycle of a resource with private state"""
        resource_name = "test_private_state"
        hub.register("resource", resource_name, TestPrivateStateResource)

        try:
            schema = TestPrivateStateResource.get_schema()

            # Plan Phase
            raw_config = {"name": "test-resource"}
            config_dv = marshal(raw_config, schema=schema.block)

            plan_request = pb.PlanResourceChange.Request(
                type_name=resource_name, config=config_dv, proposed_new_state=config_dv
            )

            plan_response = await PlanResourceChangeHandler(plan_request, context=None)
            assert not plan_response.diagnostics, (
                f"Plan failed: {plan_response.diagnostics}"
            )
            assert plan_response.planned_private, "No private state returned from plan"

            # Apply Phase
            apply_request = pb.ApplyResourceChange.Request(
                type_name=resource_name,
                config=config_dv,
                planned_state=plan_response.planned_state,
                planned_private=plan_response.planned_private,
            )

            apply_response = await ApplyResourceChangeHandler(
                apply_request, context=None
            )
            assert not apply_response.diagnostics, (
                f"Apply failed: {apply_response.diagnostics}"
            )
            assert apply_response.private, "No private state returned from apply"

            final_state = unmarshal(apply_response.new_state, schema=schema.block)
            assert final_state.value["name"].value == "test-resource"
            assert final_state.value["public_id"].value == "public-test-resource"

            # Read Phase
            read_request = pb.ReadResource.Request(
                type_name=resource_name,
                current_state=apply_response.new_state,
                private=apply_response.private,
            )

            read_response = await ReadResourceHandler(read_request, context=None)
            assert not read_response.diagnostics, (
                f"Read failed: {read_response.diagnostics}"
            )

            read_state = unmarshal(read_response.new_state, schema=schema.block)
            assert read_state.value["name"].value == "test-resource"
            assert read_state.value["public_id"].value == "public-test-resource"

        finally:
            hub.unregister("resource", resource_name)

    @pytest.mark.usefixtures("provider_with_test_mode")
    @pytest.mark.asyncio
    async def test_private_state_verifier_resource_works(self, encryption_key_env):
        """Test that the existing private state verifier resource still works"""
        resource_name = "pyvider_private_state_verifier"
        hub.register("resource", resource_name, PrivateStateVerifierResource)

        try:
            schema = PrivateStateVerifierResource.get_schema()
            raw_config = {"input_value": "test-verification"}
            config_dv = marshal(raw_config, schema=schema.block)

            plan_request = pb.PlanResourceChange.Request(
                type_name=resource_name, config=config_dv, proposed_new_state=config_dv
            )

            plan_response = await PlanResourceChangeHandler(plan_request, context=None)
            assert not plan_response.diagnostics
            assert plan_response.planned_private

            apply_request = pb.ApplyResourceChange.Request(
                type_name=resource_name,
                config=config_dv,
                planned_state=plan_response.planned_state,
                planned_private=plan_response.planned_private,
            )

            apply_response = await ApplyResourceChangeHandler(
                apply_request, context=None
            )
            assert not apply_response.diagnostics

            final_state = unmarshal(apply_response.new_state, schema=schema.block)
            assert final_state.value["input_value"].value == "test-verification"
            assert (
                final_state.value["decrypted_token"].value
                == "SECRET_FOR_TEST-VERIFICATION"
            )

        finally:
            hub.unregister("resource", resource_name)


# Tests for TimedToken Resource
class TestTimedTokenResource(FoundationTestCase):
