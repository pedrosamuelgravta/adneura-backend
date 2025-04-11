from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.models import Brand
from api.serializers import BrandSerializer


class BrandView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        brands = Brand.objects.filter(user=user.id)
        id = request.query_params.get("id")

        if id is not None:
            try:
                brand = Brand.objects.get(id=id)
                brand_serializer = BrandSerializer(brand)
                return Response(brand_serializer.data, status=status.HTTP_200_OK)
            except Brand.DoesNotExist:
                return Response(
                    {"error": "Brand not found."}, status=status.HTTP_404_NOT_FOUND
                )

        brand_serializer = BrandSerializer(brands, many=True)
        return Response(brand_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        brand_name = request.data.get("brand_name")
        brand_url = request.data.get("brand_url")

        if not brand_name:
            return Response(
                {"error": "Brand name is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        brand = Brand.objects.create(user=user, name=brand_name, brand_url=brand_url)

        brand_serializer = BrandSerializer(brand)
        return Response(brand_serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        brand_id = request.data.get("id")

        if not brand_id:
            return Response(
                {"error": "Brand ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            brand = Brand.objects.get(id=brand_id)
            brand_name = request.data.get("brand_name", brand.name)
            brand_url = request.data.get("brand_url", brand.brand_url)
            brand_summary_active = request.data.get(
                "brand_summary_active", brand.brand_summary_active
            )
            ad_legacy_active = request.data.get(
                "ad_legacy_active", brand.ad_legacy_active
            )
            strategic_goals_active = request.data.get(
                "strategic_goals_active", brand.strategic_goals_active
            )

            audience_active = request.data.get("audience_active", brand.audience_active)
            informations_active = request.data.get(
                "informations_active", brand.informations_active
            )

            brand.name = brand_name
            brand.brand_url = brand_url
            brand.brand_summary_active = brand_summary_active
            brand.ad_legacy_active = ad_legacy_active
            brand.strategic_goals_active = strategic_goals_active
            brand.audience_active = audience_active
            brand.informations_active = informations_active
            brand.save()

            brand_serializer = BrandSerializer(brand)
            return Response(brand_serializer.data, status=status.HTTP_200_OK)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Brand not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        brand_id = request.data.get("brand_id")

        if not brand_id:
            return Response(
                {"error": "Brand ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            brand = Brand.objects.get(id=brand_id)
            brand.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Brand not found."}, status=status.HTTP_404_NOT_FOUND
            )
