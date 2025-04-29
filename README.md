# Amazon Comments Ranking

![Project Status](https://img.shields.io/badge/Status-Development%20Phase-yellow)

## 📖 Overview
**Objective**  
The goal of this project is to develop a large-scale model capable of ranking product reviews — including those lacking direct customer feedback — based on a computed helpfulness index. This system is designed to enhance users' shopping experiences by promoting the most valuable and informative reviews.

**Methodology**  
We began by collecting historical Amazon review data from Kaggle and preprocessing it to establish a foundational training set. The helpfulness index for each review was calculated according to the following formula:  

Helpfulness Index equals the difference between the number of helpful votes and unhelpful votes, divided by the total number of votes.  

To further expand and diversify our dataset, we developed a custom web scraping tool that retrieves the top 100 reviews for each star rating (e.g., 5-star, 4-star, etc.) associated with every product.  

Initial attempts at review vectorization utilized Word2Vec.

  However, we identified limitations, as Word2Vec captures only individual word-level semantics without accounting for broader contextual relationships, potentially introducing logical inconsistencies.  

Through iterative experimentation, we determined that employing BERT for contextualized text embeddings, combined with XGBoost for supervised learning, significantly improved model accuracy and the quality of review ranking.

**Model Architecture**
1. **BERT Embeddings**: Capture sentence-level semantics, text -> vectors
2. **XGBoost Classifier**: Predict review helpfulness score
3. **Ranking**: Order reviews by predicted scores

## ✨ Key Features
- **Dynamic Helpfulness Scoring**: Algorithmically calculates review value.
- **Star-Rating Balanced Scraping**: Collects top 100 reviews per star rating (1–5 stars).
- **Context-Aware Model**: Combines BERT embeddings with XGBoost for ranking.
- **Browser Integration**: Chrome extension for real-time rankings and sraping.
- **Local API**: Allow communications between python and JavaScript.

## 🛠️ Installation
### Requirements
- Python libraries: 
  - pandas numpy transformers xgboost scikit-learn beautifulsoup selenium
- Browser: Chrome (for extension deployment)


### Setup
1. Clone this repository
2. Enable Chrome browser DevTools
3. Load CommentRankExtension as unpacked extension


## 🌐 Deployment
- **Target Platform**: Amazon
- **User Flow**:  
1. Install extension  
2. Run api.py on you local machine
3. Browse products  
4. Click the icon of the extension and click "Refresh Reviews" button