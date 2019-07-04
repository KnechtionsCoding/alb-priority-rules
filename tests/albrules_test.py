import pytest
from botocore.stub import Stubber

from src.albrules import show_priority

@pytest.fixture(autouse=True)
def elbv2_stub():
    with Stubber(elbv2.meta.client) as stubber:
        yield stubber
        stubber.asster_no_pending_responses()

def test_show_priority(elbv2_stub):
    elbv2_stub.add_response(
        
    )