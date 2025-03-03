# TO-DO set up payment gateway on AuthorizeNet

import env
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController
from decimal import Decimal


def get_transaction_id():
    return env.secret("TRANSACTION_ID")


def get_api_login_id():
    return env.secret("PAY_LOGIN_ID")


class CreditCard:
    number = None
    expiration_date = None
    code = None


class TransactionResponse:
    is_success = False
    messages = []


def charge_credit_card(card, amount):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = get_api_login_id()
    merchant_auth.transactionKey = get_transaction_id()

    credit_card = apicontractsv1.creditCardType()
    credit_card.cardNumber = card.number
    credit_card.expirationDate = card.expiration_date
    credit_card.cardCode = card.code

    payment = apicontractsv1.paymentType()
    payment.creditCard = credit_card

    transaction_request = apicontractsv1.transactionRequestType()
    transaction_request.transactionType = "authCaptureTransaction"
    transaction_request.amount = Decimal(amount)
    transaction_request.payment = payment

    request = apicontractsv1.createTransactionRequest()
    request.merchantAuthentication = merchant_auth
    request.refId = "MerchantID-0001"
    request.transactionRequest = transaction_request

    transaction_controller = createTransactionController(request)
    transaction_controller.execute()

    api_response = transaction_controller.getresponse()
    response = response_mapper(api_response)
    return response


def response_mapper(api_response):
    response = TransactionResponse()

    if api_response is None:
        response.messages.append("No response from api")
        return response

    if api_response.messages.resultCode == "Ok":
        response.is_success = hasattr(api_response.transactionResponse, "messages")
        if response.is_success:
            response.messages.append(
                f"Successfully created transaction with Transaction ID: {api_response.transactionResponse.transId}"
            )
            response.messages.append(
                f"Transaction Response Code: {api_response.transactionResponse.responseCode}"
            )
            response.messages.append(
                f"Message Code: {api_response.transactionResponse.messages.message[0].code}"
            )
            response.messages.append(
                f"Description: {api_response.transactionResponse.messages.message[0].description}"
            )
        else:
            if hasattr(api_response.transactionResponse, "errors") is True:
                response.messages.append(
                    f"Error Code:  {api_response.transactionResponse.errors.error[0].errorCode}"
                )
                response.messages.append(
                    f"Error message: {api_response.transactionResponse.errors.error[0].errorText}"
                )
        return response

    response.is_success = False
    response.messages.append(f"response code: {api_response.messages.resultCode}")
    return response
