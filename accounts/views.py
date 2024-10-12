# from rest_framework.response import Response
# from rest_framework.views import APIView
# from social_django.utils import load_strategy
# from social_core.backends.google import GoogleOAuth2
# from djoser.social.token import get_access_token


# class GoogleLogin(APIView):
#     def post(self, request):
#         strategy = load_strategy(request)
#         backend = GoogleOAuth2(strategy=strategy)
#         token = request.data.get('access_token')

#         try:
#             user = backend.do_auth(token)
#             if user and user.is_active:
#                 access_token = get_access_token(user)
#                 return Response({"token": access_token})
#             return Response({"error": "Authentication failed"}, status=400)
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)
