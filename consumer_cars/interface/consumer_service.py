import json
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from weightage.ml_weight import mark_best
from rest_framework.response import Response
from consumer_cars.common.request_client import RequestClient    


def get_product_full_data(listing_ids):
    result = []
    for listing_id in listing_ids:
        url = f"https://api.spinny.com/sp-consumer-search/api/c/listings/{listing_id}/product_full_details/"
        try:
            response = RequestClient.make_request(
                            url=url, method="GET", service_name='consumer-listing')
            if response.status_code != HTTP_200_OK:
                result = {"success": False, "data": "Something went wrong"}
                return result
            #just need to expose the data to frontend
            data = json.loads(response.text)
            result.append(data.get('productDetail'))
        except Exception as e:
            result = {"success": False, "data":str(e)}
            return result
    result = mark_best(result)
    final_result = {"success": "success", "data":result}
    return final_result