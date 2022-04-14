from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import requests
import time
from django.views.decorators.http import require_GET, require_POST
from users.forms import ValueForm
from .models import Stock, Portfolio


#Страница детального отображения акции с графиком
def detail_page(request, stock_name):
    form = ValueForm()
    stock = get_object_or_404(Stock, name=stock_name)
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=5min&apikey=X3X08NCFX3EY2HW3'
    response = requests.get(url.format(stock.name)).json()
    try:
        prices = response['Time Series (5min)']
    except KeyError:
        time.sleep(15)
        response = requests.get(url.format(stock.name)).json()
        prices = response['Time Series (5min)']
    price = prices[list(prices.keys())[0]][list(prices[list(prices.keys())[0]].keys())[3]]
    stock.price = float(price)
    stock.save()
    try:
        portfolio = Portfolio.objects.get(user=request.user, stock__name=stock_name)
        context = {'stock': stock, 'price': price, 'buy_form': form, 'sell_form': form, 'portfolio': portfolio}
    except Portfolio.DoesNotExist:
        context = {'stock': stock, 'price': price,'buy_form': form, 'sell_form': form}
    return render(request, 'exchangeapp/index.html', context)

#детальный респонз
@require_GET
def detail(request, stock_id):
    print('ФУНКЦИЯ СРАБОТАЛА')
    api_key = 'X3X08NCFX3EY2HW3'
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=5min&apikey=X3X08NCFX3EY2HW3'

    stock = get_object_or_404(Stock, pk=stock_id)

    all_stocks = []
    all_s = {}

    response = requests.get(url.format(stock.name)).json()
    print('респонз прошел')
    data_all = []
    for time, price in response['Time Series (5min)'].items():
        open = price['1. open']
        high = price['2. high']
        low = price['3. low']
        close = price['4. close']
        data = [time, float(low), float(open), float(close), float(high)]
        data_all.append(data)
        all_s.update({time: data})
        data_all.sort(reverse=False)
    return JsonResponse(data_all[40:], safe=False)

#главная страница
def main_page(request):
    a = []
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=5min&apikey=X3X08NCFX3EY2HW3'
    stocks = Stock.objects.all()
    for stock in stocks:
        print('-----------------------------------------------------------------------------------------------------------------------------------------')
        response = requests.get(url.format(stock.name)).json()
        try:
            price = response['Time Series (5min)']
        except KeyError:
            url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=5min&apikey=FJEPU2CGUIUM6BRG'
            response = requests.get(url.format(stock.name)).json()
            price = response['Time Series (5min)']
        price = response['Time Series (5min)']
        last_r = response['Meta Data']['3. Last Refreshed']
        dict = {
            'name': response['Meta Data']['2. Symbol'],
            'price': price[last_r]['4. close'],
        }
        a.append(dict)
    context = {'all_info': a}
    return render(request, 'exchangeapp/main.html', context)

#главная страница, получение данных из API
@require_GET
def main(request):
        a = {}
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=5min&apikey=FJEPU2CGUIUM6BRG'
        stocks = Stock.objects.all().order_by('name')
        for stock in stocks:
            try:
                response = requests.get(url.format(stock.name)).json()
            except KeyError:
                time.sleep(15)
                response = requests.get(url.format(stock.name)).json()
            print(response)
            price = response['Time Series (5min)']
            last_r = response['Meta Data']['3. Last Refreshed']
            dict = {
                'name': response['Meta Data']['2. Symbol'],
                'price': price[last_r]['4. close'],
            }
            a.update({response['Meta Data']['2. Symbol']: price[last_r]['4. close']})
        return JsonResponse(a)

#Покупка акций
@require_POST
def buy(request,stock_id,user_id):
    quantity = request.POST['value']
    stock = Stock.objects.get(pk=stock_id)
    user = request.user
    try:
        portfolio = Portfolio.objects.get(user=request.user, stock=stock)
    except Portfolio.DoesNotExist:
        portfolio = Portfolio.objects.create(user=request.user, stock=stock)
    if (float(user.money) - int(quantity)*float(stock.price)) < 0:
        return HttpResponse('На балансе не достаточно средств, пополните баланс:<ссылка на пополнение>')
    user.money = float(user.money) - int(quantity)*float(stock.price)
    user.save()
    portfolio.quantity = int(portfolio.quantity)+int(quantity)
    portfolio.total_price = float(portfolio.total_price)+float(stock.price)*int(quantity)
    portfolio.save()
    return redirect(detail_page, stock.name)


#Продажа акций
@require_POST
def sell(request,stock_id,user_id):
    quantity = request.POST['value']
    stock = Stock.objects.get(pk=stock_id)
    user = request.user
    try:
        portfolio = Portfolio.objects.get(user=request.user, stock=stock)
    except Portfolio.DoesNotExist:
        return HttpResponse('Вы продаете больше акций, чем покупаете')
    if (int(portfolio.quantity)-int(quantity)) < 0:
        return HttpResponse('Вы продаете больше акций, чем покупаете')
    user.money = float(user.money) + int(quantity)*float(stock.price)
    user.save()
    portfolio.quantity = int(portfolio.quantity)-int(quantity)
    portfolio.total_price = float(portfolio.total_price) - float(stock.price) * int(quantity)
    portfolio.save()
    return redirect(detail_page, stock.name)


#Страница с портфелем
def portfolio_page(request):
    total_price = 0
    portfolio = Portfolio.objects.filter(user=request.user)
    for port in portfolio:
        total_price += port.total_price
    context = {'portfolio_list': portfolio, 'total_price': total_price}
    return render(request, 'exchangeapp/prof.html', context)





