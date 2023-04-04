import pandas as pd
import ktrain
import eli5
import jieba
import pickle

#中文分词
def tokenization_text(text):
    tokenized_text = ' '.join(jieba.cut(text))
    return tokenized_text

def lr_explain(model, vec, sentence):
    return eli5.show_prediction(model, tokenization_text(sentence), vec=vec, feature_names=vec.get_feature_names_out())

def PredictRate(text, type='bert', v=False):
    if type == 'lr':
        with open('models/LR/rate/model_rate_LR.pickle','rb') as f:  
            model_rate_LR = pickle.load(f)
        with open('models/LR/rate/tv_model.pickle','rb') as f:  
            tv_rate = pickle.load(f)

        result = model_rate_LR.predict(tv_rate.transform([tokenization_text(text)]))
        proba = model_rate_LR.predict_proba(tv_rate.transform([tokenization_text(text)]))
        
        if result[0] == '1':
            display(pd.DataFrame([['积极', proba[0][1]]], columns=['情感', '概率']).style.set_caption("评论文本情感"))
        elif result[0] == '-1':
            display(pd.DataFrame([['消极', proba[0][0]]], columns=['情感', '概率']).style.set_caption("评论文本情感"))
        else:
            print("错误！")

        if v:
            feature = lr_explain(model_rate_LR, tv_rate, text)
            display(feature)
            
    elif type == 'bert':
        model_bert = ktrain.load_predictor('models/BERT/rate')
        predictor_bert = ktrain.get_predictor(model_bert.model, model_bert.preproc)
        
        result = predictor_bert.predict([text])
        proba = predictor_bert.predict_proba([text])
        
        if result[0] == '1':
            display(pd.DataFrame([['积极', proba[0][1]]], columns=['情感', '概率']).style.set_caption("评论文本情感"))
        elif result[0] == '-1':
            display(pd.DataFrame([['消极', proba[0][0]]], columns=['情感', '概率']).style.set_caption("评论文本情感"))
        else:
            print("错误！")
        
        if v:
            feature = predictor_bert.explain(text)
            display(feature)
            
    else: 
        print('Wrong type!')
            
def PredictExist(text, type='bert', v=False):
    if type == 'lr':
        with open('models/LR/tags/exist/model_Location_LR.pickle','rb') as f:  
            model_Location_exist_LR = pickle.load(f)
        with open('models/LR/tags/exist/tv_1_model.pickle','rb') as f:  
            tv_1_tags_exist = pickle.load(f)
            
        with open('models/LR/tags/exist/model_Service_LR.pickle','rb') as f:  
            model_Service_exist_LR = pickle.load(f)
        with open('models/LR/tags/exist/tv_2_model.pickle','rb') as f:  
            tv_2_tags_exist = pickle.load(f)
            
        with open('models/LR/tags/exist/model_Price_LR.pickle','rb') as f:  
            model_Price_exist_LR = pickle.load(f)
        with open('models/LR/tags/exist/tv_3_model.pickle','rb') as f:  
            tv_3_tags_exist = pickle.load(f)
            
        with open('models/LR/tags/exist/model_Ambience_LR.pickle','rb') as f:  
            model_Ambience_exist_LR = pickle.load(f)
        with open('models/LR/tags/exist/tv_4_model.pickle','rb') as f:  
            tv_4_tags_exist = pickle.load(f)
            
        with open('models/LR/tags/exist/model_Food_LR.pickle','rb') as f:  
            model_Food_exist_LR = pickle.load(f)
        with open('models/LR/tags/exist/tv_5_model.pickle','rb') as f:  
            tv_5_tags_exist = pickle.load(f)
    
        result_1 = model_Location_exist_LR.predict(tv_1_tags_exist.transform([tokenization_text(text)]))
        proba_1 = model_Location_exist_LR.predict_proba(tv_1_tags_exist.transform([tokenization_text(text)]))
        
        result_2 = model_Service_exist_LR.predict(tv_2_tags_exist.transform([tokenization_text(text)]))
        proba_2 = model_Service_exist_LR.predict_proba(tv_2_tags_exist.transform([tokenization_text(text)]))
        
        result_3 = model_Price_exist_LR.predict(tv_3_tags_exist.transform([tokenization_text(text)]))
        proba_3 = model_Price_exist_LR.predict_proba(tv_3_tags_exist.transform([tokenization_text(text)]))
        
        result_4 = model_Ambience_exist_LR.predict(tv_4_tags_exist.transform([tokenization_text(text)]))
        proba_4 = model_Ambience_exist_LR.predict_proba(tv_4_tags_exist.transform([tokenization_text(text)]))

        result_5 = model_Food_exist_LR.predict(tv_5_tags_exist.transform([tokenization_text(text)]))
        proba_5 = model_Food_exist_LR.predict_proba(tv_5_tags_exist.transform([tokenization_text(text)]))
        
        name_list = ['位置', '服务', '价格', '环境', '食物']
        result_list = [result_1, result_2, result_3, result_4, result_5]
        proba_list = [proba_1, proba_2, proba_3, proba_4, proba_5]
        output_list = []
        output_name_list = []
        for i in range(len(name_list)):
            if result_list[i] == '1':
                output_list.append([name_list[i], proba_list[i][0][1]])
                output_name_list.append(name_list[i])
        display(pd.DataFrame(output_list, columns=['类别', '概率']).style.set_caption("情感显著的类别"))
        
        if v:
            feature_1 = lr_explain(model_Location_exist_LR, tv_1_tags_exist, text)
            feature_2 = lr_explain(model_Service_exist_LR, tv_2_tags_exist, text)
            feature_3 = lr_explain(model_Price_exist_LR, tv_3_tags_exist, text)
            feature_4 = lr_explain(model_Ambience_exist_LR, tv_4_tags_exist, text)
            feature_5 = lr_explain(model_Food_exist_LR, tv_5_tags_exist, text)
            display(feature_1, feature_2, feature_3, feature_4, feature_5)
        
        return output_name_list
            
    elif type == 'bert':
        model_bert = ktrain.load_predictor('models/BERT/tags/exist/Location')
        predictor_bert = ktrain.get_predictor(model_bert.model, model_bert.preproc)
        
        result_1 = predictor_bert.predict([text])
        proba_1 = predictor_bert.predict_proba([text])
        
        model_bert = ktrain.load_predictor('models/BERT/tags/exist/Service')
        predictor_bert = ktrain.get_predictor(model_bert.model, model_bert.preproc)
        
        result_2 = predictor_bert.predict([text])
        proba_2 = predictor_bert.predict_proba([text])
        
        model_bert = ktrain.load_predictor('models/BERT/tags/exist/Price')
        predictor_bert = ktrain.get_predictor(model_bert.model, model_bert.preproc)
        
        result_3 = predictor_bert.predict([text])
        proba_3 = predictor_bert.predict_proba([text])
        
        model_bert = ktrain.load_predictor('models/BERT/tags/exist/Ambience')
        predictor_bert = ktrain.get_predictor(model_bert.model, model_bert.preproc)
        
        result_4 = predictor_bert.predict([text])
        proba_4 = predictor_bert.predict_proba([text])
        
        model_bert = ktrain.load_predictor('models/BERT/tags/exist/Food')
        predictor_bert = ktrain.get_predictor(model_bert.model, model_bert.preproc)
        
        result_5 = predictor_bert.predict([text])
        proba_5 = predictor_bert.predict_proba([text])
        
        name_list = ['位置', '服务', '价格', '环境', '食物']
        result_list = [result_1, result_2, result_3, result_4, result_5]
        proba_list = [proba_1, proba_2, proba_3, proba_4, proba_5]
        output_list = []
        output_name_list = []
        for i in range(len(name_list)):
            if result_list[i][0] == '1':
                output_list.append([name_list[i], proba_list[i][0][1]])
                output_name_list.append(name_list[i])
        display(pd.DataFrame(output_list, columns=['类别', '概率']).style.set_caption("情感显著的类别"))
        
        if v:
            feature_1 = predictor_bert.explain(text)
            feature_2 = predictor_bert.explain(text)
            feature_3 = predictor_bert.explain(text)
            feature_4 = predictor_bert.explain(text)
            feature_5 = predictor_bert.explain(text)
            display(feature_1, feature_2, feature_3, feature_4, feature_5)
        
        return output_name_list

    else:
        print('Wrong type!')

def PredictSenti(text, exist_name_list, type='bert', v=False):
    output_list = []
    feature_list = []
    if type == 'bert':
        if '位置' in exist_name_list:
            model_bert = ktrain.load_predictor('models/BERT/tags/senti/Location')
            predictor_bert = ktrain.get_predictor(model_bert.model, model_bert.preproc)
            
            result_1 = predictor_bert.predict([text])
            proba_1 = predictor_bert.predict_proba([text])
            if v:
                feature_1 = predictor_bert.explain(text)
                feature_list.append(feature_1)
                
            if result_1[0] == '1':
                output_list.append(['积极', proba_1[0][1]])
            elif result_1[0] == '-1':
                output_list.append(['消极', proba_1[0][0]])
            
        if '服务' in exist_name_list:
            model_bert = ktrain.load_predictor('models/BERT/tags/senti/Service')
            predictor_bert = ktrain.get_predictor(model_bert.model, model_bert.preproc)
            
            result_2 = predictor_bert.predict([text])
            proba_2 = predictor_bert.predict_proba([text])
            if v:
                feature_2 = predictor_bert.explain(text)
                feature_list.append(feature_2)
            
            if result_2[0] == '1':
                output_list.append(['积极', proba_2[0][1]])
            elif result_2[0] == '-1':
                output_list.append(['消极', proba_2[0][0]])
        
        if '价格' in exist_name_list:
            model_bert = ktrain.load_predictor('models/BERT/tags/senti/Ambience')
            predictor_bert = ktrain.get_predictor(model_bert.model, model_bert.preproc)
            
            result_3 = predictor_bert.predict([text])
            proba_3 = predictor_bert.predict_proba([text])
            if v:
                feature_3 = predictor_bert.explain(text)
                feature_list.append(feature_3)
            
            if result_3[0] == '1':
                output_list.append(['积极', proba_3[0][1]])
            elif result_3[0] == '-1':
                output_list.append(['消极', proba_3[0][0]])
        
        if '环境' in exist_name_list:
            model_bert = ktrain.load_predictor('models/BERT/tags/senti/Price')
            predictor_bert = ktrain.get_predictor(model_bert.model, model_bert.preproc)
            
            result_4 = predictor_bert.predict([text])
            proba_4 = predictor_bert.predict_proba([text])
            if v:
                feature_4 = predictor_bert.explain(text)
                feature_list.append(feature_4)
                
            if result_4[0] == '1':
                output_list.append(['积极', proba_4[0][1]])
            elif result_4[0] == '-1':
                output_list.append(['消极', proba_4[0][0]])

        if '食物' in exist_name_list:
            model_bert = ktrain.load_predictor('models/BERT/tags/senti/Food')
            predictor_bert = ktrain.get_predictor(model_bert.model, model_bert.preproc)
            
            result_5 = predictor_bert.predict([text])
            proba_5 = predictor_bert.predict_proba([text])
            if v:
                feature_5 = predictor_bert.explain(text)
                feature_list.append(feature_5)
                
            if result_5[0] == '1':
                output_list.append(['积极', proba_5[0][1]])
            elif result_5[0] == '-1':
                output_list.append(['消极', proba_5[0][0]])
        
        display(pd.DataFrame(output_list, columns=['情感', '概率'],index=exist_name_list).style.set_caption("类别情感值"))
        if v:
            for feature in feature_list:
                display(feature)
        
    elif type == 'lr':
        if '位置' in exist_name_list:
            with open('models/LR/tags/senti/model_Location_LR.pickle','rb') as f:  
                model_Location_senti_LR = pickle.load(f)
            with open('models/LR/tags/senti/tv_1_model.pickle','rb') as f:  
                tv_1_tags_senti = pickle.load(f)
            
            result_1 = model_Location_senti_LR.predict(tv_1_tags_senti.transform([tokenization_text(text)]))
            proba_1 = model_Location_senti_LR.predict_proba(tv_1_tags_senti.transform([tokenization_text(text)]))
            if v:
                feature_1 = lr_explain(model_Location_senti_LR, tv_1_tags_senti, text)
                feature_list.append(feature_1)
                
            if result_1 == '1':
                output_list.append(['积极', proba_1[0][1]])
            elif result_1 == '-1':
                output_list.append(['消极', proba_1[0][0]])
            
        if '服务' in exist_name_list:
            with open('models/LR/tags/senti/model_Service_LR.pickle','rb') as f:  
                model_Service_senti_LR = pickle.load(f)
            with open('models/LR/tags/senti/tv_2_model.pickle','rb') as f:  
                tv_2_tags_senti = pickle.load(f)
                
            result_2 = model_Service_senti_LR.predict(tv_2_tags_senti.transform([tokenization_text(text)]))
            proba_2 = model_Service_senti_LR.predict_proba(tv_2_tags_senti.transform([tokenization_text(text)]))
            if v:
                feature_2 = lr_explain(model_Service_senti_LR, tv_2_tags_senti, text)
                feature_list.append(feature_2)
                
            if result_2 == '1':
                output_list.append(['积极', proba_2[0][1]])
            elif result_2 == '-1':
                output_list.append(['消极', proba_2[0][0]])
        
        if '价格' in exist_name_list:
            with open('models/LR/tags/senti/model_Price_LR.pickle','rb') as f:  
                model_Price_senti_LR = pickle.load(f)
            with open('models/LR/tags/senti/tv_3_model.pickle','rb') as f:  
                tv_3_tags_senti = pickle.load(f)
            result_3 = model_Price_senti_LR.predict(tv_3_tags_senti.transform([tokenization_text(text)]))
            proba_3 = model_Price_senti_LR.predict_proba(tv_3_tags_senti.transform([tokenization_text(text)]))
            if v:
                feature_3 = lr_explain(model_Price_senti_LR, tv_3_tags_senti, text)
                feature_list.append(feature_3)
                
            if result_3 == '1':
                output_list.append(['积极', proba_3[0][1]])
            elif result_3 == '-1':
                output_list.append(['消极', proba_3[0][0]])
        
        if '环境' in exist_name_list:
            with open('models/LR/tags/senti/model_Ambience_LR.pickle','rb') as f:  
                model_Ambience_senti_LR = pickle.load(f)
            with open('models/LR/tags/senti/tv_4_model.pickle','rb') as f:  
                tv_4_tags_senti = pickle.load(f)
                
            result_4 = model_Ambience_senti_LR.predict(tv_4_tags_senti.transform([tokenization_text(text)]))
            proba_4 = model_Ambience_senti_LR.predict_proba(tv_4_tags_senti.transform([tokenization_text(text)]))
            if v:
                feature_4 = lr_explain(model_Ambience_senti_LR, tv_4_tags_senti, text)
                feature_list.append(feature_4)
                
            if result_4 == '1':
                output_list.append(['积极', proba_4[0][1]])
            elif result_4 == '-1':
                output_list.append(['消极', proba_4[0][0]])

        if '食物' in exist_name_list:
            with open('models/LR/tags/senti/model_Food_LR.pickle','rb') as f:  
                model_Food_senti_LR = pickle.load(f)
            with open('models/LR/tags/senti/tv_5_model.pickle','rb') as f:  
                tv_5_tags_senti = pickle.load(f)
                
            result_5 = model_Food_senti_LR.predict(tv_5_tags_senti.transform([tokenization_text(text)]))
            proba_5 = model_Food_senti_LR.predict_proba(tv_5_tags_senti.transform([tokenization_text(text)]))
            if v:
                feature_5 = lr_explain(model_Food_senti_LR, tv_5_tags_senti, text)
                feature_list.append(feature_5)
                
            if result_5 == '1':
                output_list.append(['积极', proba_5[0][1]])
            elif result_5 == '-1':
                output_list.append(['消极', proba_5[0][0]])
        
        display(pd.DataFrame(output_list, columns=['情感', '概率'],index=exist_name_list).style.set_caption("类别情感值"))
        if v:
            for feature in feature_list:
                display(feature)
                
    else:
        print('Wrong type!')

    
def Predict(text, type='bert', v=False):
    if type == 'bert':
        print('加载BERT模型')
    elif type == 'lr':
        print('加载LR模型')
    else:
        print('Wrong type!')
    
    PredictRate(text, type=type, v=v)
    exist_name_list = PredictExist(text, type=type, v=v)
    PredictSenti(text, exist_name_list, type=type, v=v)