# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 11:35:32 2018

@author: Xu Yuefangzhou

@description：使用必应翻译api直接翻译LocaleResource_en_US.properties，生成LocaleResource_zh_CN.properties
"""

import http.client, uuid, json, re

class BingFanyi:
    # @description: 该类的主功能函数为translate()，可向必应翻译api发送POST请求，得到翻译的结果。
    def __init__(self, ToLanguage):
        # @param string ToLanguage 目标语言相应代码
        self.host = 'api.cognitive.microsofttranslator.com'
        self.path = '/translate?api-version=3.0'
        self.subscriptionKey = '28e9da06f8934771acf00c01029d2f9d'   #应用subscriptionKey，失效请自行申请更换
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.subscriptionKey,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        self.ToLanguage = ToLanguage  
        self.supported_languages = { 
        #必应翻译api支持语言，可参考：http://msdn.microsoft.com/en-us/library/hh456380.aspx
            'ar' : ' Arabic',
            'bg' : 'Bulgarian',
            'ca' : 'Catalan',
            'zh-CHS' : 'Chinese (Simplified)',
            'zh-CHT' : 'Chinese (Simplified)',
            'zh-Hans': 'Chinese (Simplified)',
            'cs' : 'Czech',
            'da' : 'Danish',
            'nl' : 'Dutch',
            'en' : 'English',
            'et' : 'Estonian',
            'fi' : 'Finnish',
            'fr' : 'French',
            'de' : 'German',
            'el' : 'Greek',
            'ht' : 'Haitian Creole',
            'he' : 'Hebrew',
            'hi' : 'Hindi',
            'hu' : 'Hungarian',
            'id' : 'Indonesian',
            'it' : 'Italian',
            'ja' : 'Japanese',
            'ko' : 'Korean',
            'lv' : 'Latvian',
            'lt' : 'Lithuanian',
            'mww' : 'Hmong Daw',
            'no' : 'Norwegian',
            'pl' : 'Polish',
            'pt' : 'Portuguese',
            'ro' : 'Romanian',
            'ru' : 'Russian',
            'sk' : 'Slovak',
            'sl' : 'Slovenian',
            'es' : 'Spanish',
            'sv' : 'Swedish',
            'th' : 'Thai',
            'tr' : 'Turkish',
            'uk' : 'Ukrainian',
            'vi' : 'Vietnamese',
         }
                
    def translate (self, queryText):
        # @description:向api服务器发送请求，得到翻译结果
        # @param string queryText 待翻译内容
        # @return:若请求微软api服务器失败，则返回0。
        requestBody = [{
            'Text' : queryText,
        }]
        queryText = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')
        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request ("POST", self.path + "&to=" + self.ToLanguage, queryText, self.headers)
            response = conn.getresponse ()
            result = response.read () 
            output = json.dumps(json.loads(result.decode('utf-8')), indent=4, ensure_ascii=False)
            d=eval(output)                  #eval()函数用来执行一个字符串表达式，并返回表达式的值。
            translationResult = d[0]['translations'][0]['text']
            if isinstance(translationResult, str):
                return translationResult
        except Exception as e:
            print("请求微软api服务器失败，未得到翻译结果！")
            return 0
    
    def writein (self, queryText1):
        try:        
            file = open('LocaleResource_zh_CN.properties','a') #一行一行写入
            file.writelines(queryText1)
            file.close()
        except Exception as e:
             print("将翻译结果写入文件失败！")
     
if __name__ == "__main__":
    ToLanguage= 'zh-Hans'    
    fanyi = BingFanyi(ToLanguage) #源语自动识别，译入语为中文  
    with open('LocaleResource_en_US.properties') as f: #默认模式为‘r’，只读模式
        lines=f.readlines()
        for line in lines:
            if re.match('\s',line): #这一行是空行，则直接写入
                fanyi.writein(line)
            else: #这一行不是空白行  
                if re.match('#',line): #这一行如果是以“#”开头的，则直接写入不用翻译
                    fanyi.writein(line)
					
                else:    #将每一行进行分组，分成三组：等号前、等号、等号后                
                    group1=re.search("([\w+\.?()]+)(\s*=\s*)(.*)",line).group(1)
                    group2=re.search("([\w+\.?()]+)(\s*=\s*)(.*)",line).group(2)
                    group3=re.search("([\w+\.?()]+)(\s*=\s*)(.*)",line).group(3)
    
                    if re.search('.gif',group3): #包含“.gif”的不用翻译，直接写入
                        fanyi.writein(line)
                    
                    elif re.fullmatch("\s*",group3): #等号后面没有内容的不用翻译，直接写入
                        fanyi.writein(line)
                        
                    elif re.match('timezones',group1): #key为timezones的不用翻译，直接写入
                        fanyi.writein(line)
                                              
                    elif re.search('.htm',group3): #包含“.htm”的不用翻译，直接写入
                        fanyi.writein(line)
                    
                    else:  #其他的翻译等号后面的内容
                        fanyi.writein(group1 + group2 + fanyi.translate(group3) + '\n') 
                            
                        
