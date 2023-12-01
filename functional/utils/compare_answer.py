from http import HTTPStatus


def compare_answer(status, body, expected_answer):
    if status == HTTPStatus.OK:
        try:
            assert {
                'status': status,
                'length': len(body['items']),
                'page': body['page'],
                'size': body['size'],
            } == expected_answer
        except Exception:
            assert {
                'status': status,
                'id': body['id']
            } == expected_answer
    elif status == HTTPStatus.NOT_FOUND:
        assert {'status': status,
                'detail': body['detail']} == expected_answer
