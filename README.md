# product_recommendation_api
Reddit-Powered Product Recommendation System with OpenHermes 2.5 LLM based on Mistral 7B and a focus on sustainable consumption.   
**Note:** Product recommendations are generated locally, ensuring user privacy and data protection. The project requires at least 16GB of VRAM to run the [OpenHermes LLM](https://ollama.ai/library/openhermes) reliably.

## Why?

To save time and effort in researching durable goods while ensuring that you make informed decisions based on real user experiences and opinions. Also because I need it.

## Why? (but in more detail)

**Reduced consumption:** By purchasing durable, long-lasting products, users can reduce their overall consumption of goods, which in turn reduces the environmental impact of manufacturing, transportation, and disposal.

**Extended product lifespans**: When products are designed and built to last, they can be used for many years, further reducing the need for new purchases. This also helps to minimize the waste generated by discarded products.

**Support for ethical businesses:** Many of the products recommended on r/buyitforlife are made by companies that prioritise sustainable practices and ethical labor standards. By supporting these businesses, consumers can contribute to a more responsible and environmentally conscious marketplace.

**Promoting mindful consumerism:** The subreddit encourages users to consider the long-term implications of their purchases and to avoid impulse buys or purchases of disposable items. This promotes a more mindful approach to consumerism that values quality over quantity.

## Requirements

1. [Ollama](https://ollama.ai/)

## Instructions

* To prepare the environment (only on the first run)   
`chmod +x prep_environment.sh & ./prep_environment.sh`

* Get the LLM running   
`ollama run openhermes`

* Run the server   
`chmod +x run.sh & ./run.sh`


## How does it work?

![rec drawio (1)](https://github.com/smellycloud/product_recommendation_api/assets/52908667/afb80010-f687-4d48-b189-74d0de0285d7)

By extracting insights from Reddit discussions, particularly those pertaining to r/buyitforlife, the system delves into product reviews, ratings, and discussions to identify highly regarded and durable products. These insights are then fed into OpenHermes LLM, a large language model trained on a vast dataset of text. The LLM effectively processes the product information and generates a personalised recommendation list.

## Caveats

**Products are not created equal:** Simply because a product is popular on the subreddit doesn't imply that it's right for you. Always conduct your own research to ensure that a product meets your requirements.

**Consider your own budget:** The subreddit frequently suggests high-quality products that can be expensive. Make sure to consider your budget when making your decision.


## Screenshots
![4](https://github.com/smellycloud/product_recommendation_api/assets/52908667/13a6756f-b63f-40f5-8dab-8486ebc44087)
![2](https://github.com/smellycloud/product_recommendation_api/assets/52908667/195efa43-5c99-45dc-a737-c90f641a8bdb)
![1](https://github.com/smellycloud/product_recommendation_api/assets/52908667/61bc87cd-ebf5-46fd-986e-745534b3758d)
![3](https://github.com/smellycloud/product_recommendation_api/assets/52908667/b0475e64-5d48-446b-936f-d8f02af5c115)

### You get the idea...
Remember, by choosing high-quality, durable items from reputable brands with transparent manufacturing practices, you can support companies that prioritise sustainability, fair labor practices, and ethical sourcing of materials.
