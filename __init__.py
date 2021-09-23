#%%writefile app.py

import pickle

import streamlit as st

# loading the trained model
pickle_in = open('bcr_model.pkl', 'rb') 
classifier = pickle.load(pickle_in)
 
@st.cache()
  

# cols = [
#     "Current Meds", "Prior Cancer", "Percent Pos Biopsies", "Perineural Invasion",
#     "Baseline PSA Value", "T Stage", "D'Amico Risk Category", "Treatment",
#     "Age", "Gleason_Grade",
# ]
# defining the function which will make the prediction using the data which the user inputs 
def prediction(current_meds, prior_cancer, percent_pos_biopsies, perineural_invasion, psa, t_stage,\
                risk_category, treatment, age, gleason_grade):   
 
    # Pre-processing user input
    # Current meds    
    if current_meds == "Yes":
        current_meds = 1
    elif current_meds == "No":
        current_meds = 2
    else:
        current_meds = 3
    #Prior Cancer
    if prior_cancer == "Yes":
        prior_cancer = 1
    elif prior_cancer == "No":
        prior_cancer = 0
    else:
        prior_cancer = 2 # not obtained

    #perineural invasion
    if perineural_invasion == "Present":
        perineural_invasion = 1
    elif perineural_invasion == "Not Present":
        perineural_invasion = 2
    else:
        perineural_invasion = 3
    
    # T stage
    if t_stage in ["T1a", "T1b", "T1c"]:
        t_stage = 1
    elif t_stage in ["T2a", "T2b", "T2c"]:
        t_stage = 2
    elif t_stage in ["T3a", "T3b"]:
        t_stage = 3
    elif t_stage == "T4":
        t_stage = 4
    elif t_stage == "TX":
        t_stage = 5
    else: 
        t_stage = 6
    
    # D'Amico Risk Category
    if risk_category == "Low Risk":
        risk_category = 1
    elif risk_category == "Intermediate Risk":
        risk_category = 2
    else:
        risk_category = 3 # not obtained
    
    # Treatment
    if treatment == "SEED":
        treatment = 1
    elif treatment == "EBRT + SEED + ADT":
        treatment = 4
    elif treatment == "SEED + ADT":
        treatment = 2
    else:
        treatment = 3


    prediction_prob = classifier.predict_proba([[current_meds, prior_cancer, percent_pos_biopsies, perineural_invasion, psa, t_stage,\
                risk_category, treatment, age, gleason_grade]])

    print(prediction_prob)
    ix = prediction_prob.argmax(1).item()

    classes = ['Patient does not relapse', 'Patient relapses in 5 years', 'Patient relapses in 10 years']
    result_text = f'{classes[ix]} and confidence is {prediction_prob[0,ix]:.2%}'
 
    # Making predictions 
    prediction = classifier.predict( 
        [[current_meds, prior_cancer, percent_pos_biopsies, perineural_invasion, psa, t_stage,\
                risk_category, treatment, age, gleason_grade]])
     
    # if prediction == 0:
    #     pred = 'Rejected'
    # else:
    #     pred = 'Approved'
    return prediction, result_text
      
  
def main():
           
    # front end elements of the web page 
    html_temp = """ 
    <div style ="padding:13px"> 
    <h1 style ="color:black;text-align:center;">Bio-Chemical Recurrence Prediction</h1> 
    </div> 
    """
      
    # display the front end aspect
    # st.markdown(html_temp, unsafe_allow_html = True) 
    st.title("Bio-Chemical Recurrence Prediction")
    st.sidebar.title("Patient Details")
    st.sidebar.text("Please fill in the details")
    # following lines create boxes in which user can enter data required to make prediction 
    current_meds = st.sidebar.selectbox('Current Medications',("Yes", "No", "Not Obtained/Unkown"))
    prior_cancer = st.sidebar.selectbox('Prior Cancer',("Yes","No")) 
    percent_pos_biopsies = st.sidebar.slider("Positive Biopsies Percentage(%)",0.0,100.0)
    perineural_invasion = st.sidebar.selectbox('Perineural Invasion', ('Present', 'Not Present', 'Unknown'))
    psa = st.sidebar.number_input("Enter the PSA value")
    t_stage = st.sidebar.selectbox('T Stage', ('T1a','T1b', 'T1c','T2a', 'T2b', 'T2c', 'T3a', 'T3b', \
                                                    'T4', 'TX', 'Not Obtained'))
    risk_category = st.sidebar.selectbox("D'Amico Risk Category", ("Low Risk", "Intermediate Risk", "High Risk"))
    treatment = st.sidebar.selectbox('Treatment', ("SEED","EBRT + SEED + ADT","SEED + ADT", "EBRT + SEED"))
    age = st.sidebar.slider('Age',0,120)
    gleason_grade = st.sidebar.slider('Gleason Grade', 1,5)

    

    result =""



    # when 'Predict' is clicked, make the prediction and store it 
    if st.sidebar.button("Predict"): 
        result, result_text = prediction(current_meds, prior_cancer, percent_pos_biopsies, perineural_invasion, psa, t_stage,\
                risk_category, treatment, age, gleason_grade) 
        # st.success('BCR Category {}'.format(result))
        st.success('{}'.format(result_text))

        
        
     
if __name__=='__main__': 
    main()