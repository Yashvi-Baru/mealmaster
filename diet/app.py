from flask import Flask, render_template, request
import os
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain
import re

os.environ['OPENAI_API_KEY'] = '' # your openai key

app = Flask(__name__)

llm_resto = OpenAI(temperature=0.6, max_tokens=2000)
#llm_resto = OpenAI(temperature=0.6)

prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'region', 'allergy'],
    template="Diet Recommendation System:\n"
             "I want you to plan the healthy diet with 4 breakfast dishes names, 4 lunch dishes names, 4 brunch dishes names, and 4 dinner dishes names, with their local language names and small recipe description"
             "based on the following criteria:\n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight: {weight}\n"
             "Person height: {height}\n"
             "Person veg_or_nonveg: {veg_or_nonveg}\n"
             "Person region: {region}\n"
             "Person allergy: {allergy}\n"
             "Also remember not to mention any dishes related to the allergies mentioned above and its okay if you repeat 1-2 dishes"
)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/recommend', methods=['POST','GET'])
def recommend():
    if request.method == "POST":
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        veg_or_noveg = request.form['dietPreference']
        region = request.form['region']
        allergy = request.form['allergy']

        chain_resto = LLMChain(llm=llm_resto, prompt=prompt_template_resto)
        input_data = {'age': age,
                      'gender': gender,
                      'weight': weight,
                      'height': height,
                      'veg_or_nonveg': veg_or_noveg,
                      'region': region,
                      'allergy': allergy}
        #results = chain_resto.run(input_data)
        results_dict = chain_resto.invoke(input_data)  # Assuming `invoke` returns a dictionary
        results = results_dict['text']  # Assuming the text is stored under the key 'text' in the dictionary



        # Print the LangChain results for debugging
        print("LangChain Results:")
        print(results)

        # Extracting the different recommendations using regular expressions
        # breakfast_names_match = re.search(r'Breakfast:(.*?)Lunch:', results, re.DOTALL)
        # lunch_names_match = re.search(r'Lunch:(.*?)Brunch:', results, re.DOTALL)
        # brunch_names_match = re.search(r'Brunch:(.*?)Dinner:', results, re.DOTALL)
        # dinner_names_match = re.search(r'Dinner:(.*?)$', results, re.DOTALL)

        # Regular expressions to extract recommendations for each meal category
        breakfast_names_match = re.search(r'Breakfast:(.*?)(?:Lunch:|Brunch:|Dinner:|$)', results, re.DOTALL)
        lunch_names_match = re.search(r'Lunch:(.*?)(?:Brunch:|Dinner:|$)', results, re.DOTALL)
        brunch_names_match = re.search(r'Brunch:(.*?)(?:Dinner:|$)', results, re.DOTALL)
        # dinner_names_match = re.search(r'Dinner:(.*?)', results, re.DOTALL)
        dinner_names_match = re.search(r'Dinner:(.*?)$', results, re.DOTALL)



        # Debug statements to inspect extracted recommendations
        print("Extracted Breakfast:", breakfast_names_match.group(1).strip() if breakfast_names_match else "None")
        print("Extracted Lunch:", lunch_names_match.group(1).strip() if lunch_names_match else "None")
        print("Extracted Brunch:", brunch_names_match.group(1).strip() if brunch_names_match else "None")
        print("Extracted Dinner:", dinner_names_match.group(1).strip() if dinner_names_match else "None")


        # Cleaning up the extracted lists
        breakfast_names = [name.strip() for name in breakfast_names_match.group(1).strip().split('\n') if name.strip()] if breakfast_names_match else []
        lunch_names = [name.strip() for name in lunch_names_match.group(1).strip().split('\n') if name.strip()] if lunch_names_match else []
        brunch_names = [name.strip() for name in brunch_names_match.group(1).strip().split('\n') if name.strip()] if brunch_names_match else []
        dinner_names = [name.strip() for name in dinner_names_match.group(1).strip().split('\n') if name.strip()] if dinner_names_match else []

        # Debug statements to inspect cleaned lists
        print("Cleaned Breakfast:", breakfast_names)
        print("Cleaned Lunch:", lunch_names)
        print("Cleaned Brunch:", brunch_names)
        print("Cleaned Dinner:", dinner_names)

        return render_template('result.html', breakfast_names=breakfast_names, lunch_names=lunch_names, brunch_names=brunch_names, dinner_names=dinner_names)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
