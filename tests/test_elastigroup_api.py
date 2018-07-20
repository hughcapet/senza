import responses
from spotinst.components.elastigroup_api import update_capacity, get_elastigroup, SPOTINST_API_URL


def test_update_capacity(monkeypatch):
    update = {
        'response': {
            'items': [{
                'id': 'sig-xfy',
                'name': 'my-app-1',
                'capacity': {
                    'minimum': 1,
                    'maximum': 3,
                    'target': 3,
                    'unit': 'instance'
                }
            }]
        }
    }

    elastigroup_id = 'sig-xfy'
    spotinst_account_id = 'act-zwk'
    spotinst_token = 'fake-token'
    with responses.RequestsMock() as rsps:
        rsps.add(rsps.PUT,
                 '{}/aws/ec2/group/{}?accountId={}'.format(SPOTINST_API_URL, elastigroup_id, spotinst_account_id),
                 status=200,
                 json=update)

        update_response = update_capacity(1, 3, 3, elastigroup_id, spotinst_account_id, spotinst_token)
        assert update_response['id'] == elastigroup_id
        assert update_response['name'] == 'my-app-1'
        assert update_response['capacity']['minimum'] == 1
        assert update_response['capacity']['maximum'] == 3
        assert update_response['capacity']['target'] == 3


def test_get_elastigroup(monkeypatch):
    group = {
        'response': {
            'items': [{
                'id': 'sig-xfy',
                'name': 'my-app-1',
                'region': 'eu-central-1',
            }]
        }
    }

    elastigroup_id = 'sig-xfy'
    spotinst_account_id = 'act-zwk'
    spotinst_token = 'fake-token'
    with responses.RequestsMock() as rsps:
        rsps.add(rsps.GET, 'https://api.spotinst.io/aws/ec2/group/{}?accountId={}'.format(elastigroup_id, spotinst_account_id),
                 status=200,
                 json=group)

        group = get_elastigroup(elastigroup_id, spotinst_account_id, spotinst_token)
        assert group['id'] == elastigroup_id
        assert group['name'] == 'my-app-1'
