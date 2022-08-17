# AldiChecker 
Are you waiting for the price to drop at Aldi but can't keeping checking their website everyday. Intdoducing AldiChecker, it checks for you.  
Just it the url of the product and it's current price and it will notify you on the price drop.  It will send you alerts on Telegram with the price info.

## Config and set up
Set up is very minimal and simple;  

Install all requirement first by doing "pip install -r requirement.txt".

Open config.ini in config folder. Change product_url to the your product url and change base_price to the current price of the product.  
Under "telegram" section of config, add your bot token and chat id.  

Schedule your run and that's it.  

### Not sure how to get started with Telegram bot?
Try [How to Create and Connect a Telegram Chatbot](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot)

### Screenshot of the alert
![](https://github.com/tendhar33/Images/blob/e6b6d6946bbb2a555bab99f82491829c717ec2c0/Alert.png)