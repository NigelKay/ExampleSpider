# -*- coding: utf-8 -*-
import scrapy
import math

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    #CMD line input for ending of url
    ending = input("Enter URL digits: ")+".html"
    #CMD line input for cost in Euro
    cost = (input("Cost price: €"))
    #Exchange Rate: Change here!
    exchange_rate = 1.15
    start_urls = ['https://www.example.com/item'+ending]

    def parse(self, response):
        # PRICES
        costeur = float(ExampleSpider.cost)
        costpounds = round((costeur/ExampleSpider.exchange_rate),2)
        wholesale = round((costpounds*1.3),2)
        rounded_wholesale = round(math.ceil(wholesale / 0.05) * 0.05, -int(math.log10(0.005)))
        retail = round((rounded_wholesale*1.41),2)

        # FUNCTIONS
        def var1_func():
            var1 = response.css('.col-sm-9 .preview::text').extract()
            result = []
            loop = 0
            while loop < len(var1):
                result.append('<p>'+var1[loop]+'</p>\n'+'<p><example.com/'+response.css('a+ span::text').extract_first().lower()+str(int(loop)+1)+'."></example></p>\n')
                loop+=1
            return "".join(result)

       # Dicts
        product_type_dict = {'7inch':'Value','8inch':'Value','9inch':'Value','10inch':'Value','11inch':'Value','12inch':'Value'}
        product_weight_dict = {'7inch':0.225,'8inch':0.225,'9inch':0.225,'10inch':0.4,'11inch':0.4,'12inch':0.225,'15inch':0.225}
        product_selector = response.css('.nooverflow span::text').extract_first()

        # VARIABLES
        categories = ", ".join(response.css('.label-default span::text').extract())
        identifier = response.css('a+ span::text').extract_first()
        var2 = response.css('h1 a::text').extract_first()
        title = response.css('h1 + h2::text').extract_first()
        brand = response.css('.normal .table a span::text').extract_first()
        description = str("<p><em>"+response.css('p::text').extract_first()+"</em></p>\n")
        var1_html = var1_func()

        #output categories to CSV
        item = {
            #Constants
            'Supplier': "Example",
            'Stock Control': "FIFO",
            'Min Stock Level': 1,
            'Reorder Qty': 1,

            #Variables
            'Style Code': identifier,
            'Code': identifier,
            'Product Name': var2+" - "+title,
            'Brand': brand,
            'Tags': categories+", "+identifier+", "+var2+", "+brand+", "+product_selector,
            'Product Types': product_type_dict[product_selector],
            'ProductOptions-Weight': product_weight_dict[product_selector],
            'Description': description + var1_html,

            'CostEUR EUR Exempt': costeur,
            'Cost GBP Exempt': costpounds,
            'Wholesale GBP Excl': rounded_wholesale,
            'Retail GBP Excl': retail,
            }
        yield item

        #quit function to end repeats
        ExampleSpider.ending = input("Enter VAR: ")+".html"
        if ExampleSpider.ending.upper() == "QUIT.HTML":
            quit()
        else:
            #loop for multiple products
            ExampleSpider.cost = (input("Cost price: "))
            yield scrapy.Request(url="https://www.example.com/item"+ExampleSpider.ending, callback=self.parse)