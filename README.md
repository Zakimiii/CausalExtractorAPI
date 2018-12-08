# CuasalExtractorAPI

## Environment
|項目|設定|
|----|----|
|言語|Python 3.6.0|
|本番環境|AWS-Ec2| 
|バックエンド|FireBase|
|API|Django| 
|デバイス|web|


## Set up

### Causal extract from google search

````
repository = causalRepository()
extractor =  extractor()
crawlers = repository.syncCrawle("自信がつかない理由")
causals, crawlers = extractor.extract(crawlers, Relation.cause)
repository.setCausalData(causals, crawlers)
````
### Create google corpas

````
repository = causalRepository()
repository.routineCrawle("自信がつかない理由")
````

### Lex Rank Causal

````
repository.lexRankCausal(causals)
````


### CrossBootstrap

````
crossBootstrap = CrossBootstrap()
crossBootstrap.getResultExpression(causals)
crossBootstrap.getClueExpression(causal.sentence for causal in causals)
````

### AI classification and RNN , word2vec

Please see more detail in test.ipynb
