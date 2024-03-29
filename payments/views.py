from django.shortcuts import redirect
from rest_framework.views import APIView, Response
import stripe
from django.conf import settings
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET

# Create your views here.


class CreateCheckoutSession(APIView):
    def post(self, request):
        dataDict = dict(request.data)
        price = dataDict['price'][0]
        product_name = dataDict['product_name'][0]
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product_name,
                        },
                        'unit_amount': price
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url='http://127.0.0.1:8000/payment-success/',
                cancel_url='http://127.0.0.1:8000/payment-failed/',
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(e)
            return e


class PaymentSuccess(APIView):
    def get(self, request):
        return Response({'message': 'Payment Successfull'})


class PaymentFailed(APIView):
    def get(self, request):
        return Response({'message': 'Payment Failed'})


class WebHook(APIView):
    def post(self, request):
        event = None
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as err:
            # Invalid payload
            raise err
        except stripe.error.SignatureVerificationError as err:
            # Invalid signature
            raise err

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            print("--------payment_intent ---------->", payment_intent)
        elif event.type == 'payment_method.attached':
            payment_method = event.data.object
            print("--------payment_method ---------->", payment_method)
        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event.type))

        return JsonResponse(success=True, safe=False)
