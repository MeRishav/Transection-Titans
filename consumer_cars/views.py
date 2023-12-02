from rest_framework import viewsets
from rest_framework.response import Response
import os
import json
from .common.request_client import RequestClient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from weightage.ml_weight import mark_best


class ListingData(APIView):
    def get(self, request, *args, **kwargs):
        lead_id = request.query_params.get("lead_id")
        url = "https://api.spinny.com/sp-consumer-search" + f"/product/listing/{lead_id}/related/"
        try:
            params = {"count": 12, "availability":"available"}
            response = RequestClient.make_request(
                            url=url, method="GET", params=params,
                            service_name='consumer-listing')
            if response.status_code != HTTP_200_OK:
                result = {"success": False, "data": "Something went wrong"}
                return Response(result, status=response.status_code)
            #we are going to get data for multiple cars related to provided cars's id
            #need to perform ml on that and need to return data according to that with the specific flag(for which car we want
            # to show as preference 1st)
            result = {"success": True, "data": json.loads(response.text)}
            mark_best(result.get("data").get("results"))
            return Response(result, status=HTTP_200_OK)
        except Exception as e:
            result = {"success": False, "data":str(e)}
            return Response(result, status=HTTP_500_INTERNAL_SERVER_ERROR)
        

class ListingForMultipleProject(APIView):
    def get(self, request, *args, **kwargs):
        list_ids = request.query_params.get("listings_ids")
        listing_ids = list_ids.split(',')
        print(listing_ids)
        result = []
        for listing_id in listing_ids:
            url = f"https://api.spinny.com/sp-consumer-search/api/c/listings/{listing_id}/product_full_details/"
            try:
                response = RequestClient.make_request(
                                url=url, method="GET", service_name='consumer-listing')
                if response.status_code != HTTP_200_OK:
                    result = {"success": False, "data": "Something went wrong"}
                    return Response(result, status=response.status_code)
                #just need to expose the data to frontend
                data = json.loads(response.text)
                result.append(data.get('productDetail'))
            except Exception as e:
                result = {"success": False, "data":str(e)}
                return Response(result, status=HTTP_500_INTERNAL_SERVER_ERROR)
        final_result = {"success": "success", "data":result}
        mark_best(final_result.get("data"))
        return Response(final_result, status=HTTP_200_OK)