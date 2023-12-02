import json, time
import requests
import simplejson
from ..interface.constants import DEFAULT_HTTP_TIMEOUT, MAX_RETRY, REATTEMPT_INTERVAL

HTTP_ERROR = "HTTP Error "
CONNECTION_ERROR = "Connection Error "
TIMEOUT_ERROR = "Timeout Error "
REQUEST_EXCEPTION = "REQUEST EXCEPTION "
EXCEPTION = "EXCEPTION"


class RequestClient:
    
    @staticmethod
    def make_request(url, method, service_name, data=None, headers=None, params=None, json=None, timeout=DEFAULT_HTTP_TIMEOUT, 
                     call_with_retry=False, attempt: int = 1):
        """
        method – method for the new Request object: GET, OPTIONS, HEAD, POST, PUT, PATCH, or DELETE.
        url – URL for the new Request object.
        params – (optional) Dictionary, list of tuples or bytes to send in the query string for the Request.
        data – (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the Request.
        headers – (optional) Dictionary of HTTP Headers to send with the Request.
        json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
        Returns:
            response object
        """
        try:
            response = requests.request(url=url, method=method, data=data, headers=headers, params=params,
                                        json=json, timeout=timeout)
        except requests.Timeout as e:
            message = f'Timeout error. Retry attempt: {attempt}  (Timeout: {timeout} seconds) '
            if call_with_retry and attempt <= MAX_RETRY:
                time.sleep(REATTEMPT_INTERVAL)
                timeout = 2*timeout
                attempt += 1
                return RequestClient.make_request(url, method, service_name, data, headers, params, json,
                                        timeout, call_with_retry, attempt)
            response = None
        except requests.ConnectionError as e:
            message = f'Connection error. Retry attempt: {attempt} (Timeout: {timeout} seconds)'
            if call_with_retry and attempt <= MAX_RETRY:
                time.sleep(REATTEMPT_INTERVAL)
                attempt += 1
                return RequestClient.make_request(url, method, service_name, data, headers, params, json,
                                        timeout, call_with_retry, attempt)
            response = None
        except requests.HTTPError as e:
            message = f'Http error. Retry attempt: {attempt} (Timeout: {timeout} seconds)'
            if call_with_retry and attempt <= MAX_RETRY:
                time.sleep(REATTEMPT_INTERVAL)
                attempt += 1
                return RequestClient.make_request(url, method, service_name, data, headers, params, json,
                                        timeout, call_with_retry, attempt)
            response = None
        except requests.RequestException as e:
            response = None
        return response


    @staticmethod
    def process_response(response):
        """
            Method to process the responses from Auction Service.
        :param response: (object)
        :return: response_json, status_code
        """
        if not response:
            return {}, 500
        try:
            response_data = response.json()
        except simplejson.JSONDecodeError:
            response_data = response.content
        except json.JSONDecodeError:
            response_data = response.content
        status_code = response.status_code
        return response_data, status_code
