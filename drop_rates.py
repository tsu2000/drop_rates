import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from streamlit import caching
from scipy.stats import geom




def main(): # Main title
    st.title('AdventureQuest Worlds Drop Rates')
    subtitle = '### Statistics of Drop Rates in AQWorlds'
    st.markdown(subtitle)
    
    st.markdown('This web app is for the data visualisation of the drop rates in the MMORPG, AdventureQuest Worlds. Users can input the drop rate of an item and use a slider/number input to see how the probability of obtaining an item changes as the number of tries increases. Players may also view an in-depth explanation of how the drop rate probabilities are calculated by selecting the other box from the banner below.')
    
    st.components.v1.html("""<a href="https://github.com/tsu2000/drop_rates" target="_blank"><img src="https://img.shields.io/static/v1?label=tsu2000&message=drop_rates
&color=blue&logo=github" alt="_blank"></a><a href="https://github.com/tsu2000/drop_rates" target="_blank"><img src="https://img.shields.io/github/stars/tsu2000/drop_rates?style=social" alt="tsu2000 - Drop Rates"></a>""", height=28)

    topics = ['Drop Rate Calculations', 
              'In-depth explanation behind probability calculations']

    topic = st.selectbox('Select a topic: ', topics)

    if topic == topics[0]:
        calc()
    elif topic == topics[1]:
        expl()
    
    



def calc():
    st.markdown('---')
    st.markdown('## Drop Rate Calculations')
    
    st.markdown('Choose an item from the list below to get its drop rate: ')
    
    low_drop_dict = {'Burning Blade of Abezeth': 5.0,
                     "Axeros' Brooch": 4.0,
                     'Dark Unicorn Rib': 2.0,
                     'Runes of Awe': 1.0,
                     'Doom Heart': 0.5}
    
    chosen_idr = st.selectbox('Item', ['N/A'] + list(low_drop_dict.keys()))
    
    st.markdown('**OR** directly input the drop rate of an item:')
    
    prob_percent = st.number_input('Item Drop Rate (in %):', 
                           min_value = 0.01, max_value = 95.00, 
                           value = 25.00 if chosen_idr == 'N/A' else low_drop_dict[chosen_idr], 
                           step = 0.10, format = "%.2f")
    
    p = prob_percent / 100  
 
    interact_type = st.sidebar.radio('Choose the method which you would like to interact with the plots:', ['Slider', 'Number Input'])
    
    if interact_type == 'Slider':
        xi = st.sidebar.slider('Choose number of tries:', 
                               min_value = 1, 
                               max_value = int(geom.ppf(0.999, p) - 1), 
                               value = int(1/p),
                               step = 1)

    else:
        xi = st.sidebar.number_input('Choose number of tries:', 
                                     min_value = 1, 
                                     max_value = int(geom.ppf(0.999, p) - 1),
                                     value = int(1/p),
                                     step = 1)
        
    st.sidebar.markdown('**Statistics:**')
    st.sidebar.markdown(f'Expected No. of Tries: &emsp;**{int(1/p)}**  \nStandard Deviation: &emsp;**{round(np.sqrt((1-p))/p, 2)}**  \n25th Percentile: &emsp;**{int(geom.ppf(0.25, p))}**  \nMedian: &emsp;**{int(geom.ppf(0.5, p))}**  \n75th Percentile: &emsp;**{int(geom.ppf(0.75, p))}**  \n99th Percentile: &emsp;**{int(geom.ppf(0.99, p))}**')
    
    #@st.cache(allow_output_mutation = True, suppress_st_warning = True)
    def pmf():
        plt.style.use('seaborn-whitegrid')
        fig, ax = plt.subplots(figsize = (12, 6), dpi = 300)
       
        x = np.arange(1, geom.ppf(0.999, p))
        yi = geom.pmf(xi, p)

        plt.plot(x, geom.pmf(x, p), color = 'blue')
        plt.scatter(xi, yi, color = 'blue')
        plt.text(xi, yi, f'~ {round(yi, 4)}', ha = 'left', va = 'bottom', color = 'blue')

        ryi = round(yi, 6)
        textstr = "\n".join([r'Probability of obtaining item on try no. $\bf{%s}$:' % str(xi),
                             f'{ryi}' + ' (around ' + r"$\bf" + str(round(yi * 100, 2)) + "\%}$" + ')'])
        props = dict(boxstyle = 'round', facecolor = 'azure')
        plt.text(geom.ppf(0.975, p), p, textstr, fontsize = 12, va = 'top', bbox = props)

        plt.title('Individual probability of obtaining item with a ' + r"$\bf{" + str(p*100) + "\%}$" + ' drop rate')
        plt.ylabel('Probability of obtaining item')
        plt.xlabel('Try Number')
        return st.pyplot(fig)
    
    #@st.cache(allow_output_mutation = True, suppress_st_warning = True)
    def cdf():
        plt.style.use('seaborn-whitegrid')
        fig, ax = plt.subplots(figsize = (12, 6), dpi = 300)

        x = np.arange(1, geom.ppf(0.999, p))
        yi = geom.cdf(xi, p)

        plt.plot(x, geom.cdf(x, p), color = 'red')
        plt.scatter(xi, yi, color = 'red')
        plt.ylim(0, 1)

        plt.text(xi, yi, f'~ {round(yi, 4)}', ha = 'left', va = 'top', color = 'red')

        ryi = round(yi, 6)
        textstr = "\n".join([r'Probability of obtaining item by try no. $\bf{%s}$:' % str(xi),
                             f'{ryi}' + ' (around ' + r"$\bf" + str(round(yi * 100, 2)) + "\%}$" + ')'])
        props = dict(boxstyle = 'round', facecolor = 'mistyrose')
        plt.text(geom.ppf(0.975, p), 0.15, textstr, fontsize = 12, va = 'top', bbox = props)

        plt.title('Cumulative probability of obtaining item with a ' + r"$\bf{" + str(p*100) + "\%}$" + ' drop rate')
        plt.ylabel('Probability of obtaining item')
        plt.xlabel('Cumulative Number of Tries')
        return st.pyplot(fig)
    
    pmf()
    cdf()
    
    st.markdown('---')
    st.markdown('*This web app is in no way affiliated with AdventureQuest Worlds or Artix Entertainment.*')

    
    
    
def expl():
    
    st.markdown('---')
    st.markdown('## In-depth explanations behind probability calculations')

    st.markdown('This section goes into greater depth about the explanation behind the type of probability distribution used in the drop rate calculation. Folks who wish to read and understand this section should have a basic understanding of probability and statistics.')

    
    st.markdown('### Geometric Distribution')
    st.markdown('A geometric probability distribution is a type of [**discrete probability distribution**](https://www.cuemath.com/data/discrete-probability-distribution/) which measures the probability of success the first time after a given number of trials.')
    
    st.markdown('There are three assumptions involved in a geometric distribution. These are:')
    st.markdown('- There are only **two** possible outcomes (success or failure) for each trial.')
    st.markdown('- The trials are **independent** from each other. (Outcome of earlier trial does not affect probability of outcome for a later trial)')
    st.markdown('- The probability of success is the **same** for each trial.')
    
    st.markdown('Items in-game usually have a constant drop rate (e.g. 5%, 2%) and every time a monster is defeated, the probability of the item dropping does not change at all. Since most item drops in the game are consistent with these 3 assumptions, we can safely assume that the drop rates in the game can be modeled using a **geometric distribution**.')
    
    st.markdown('To show that a random variable $X$ follows a geometric distribution with probability of success $p$, the following notation is used:')
    st.latex(r'''X \sim Geo(p)''')
    
    st.markdown('Expected Value or Mean for Geometric Distribution:')
    st.latex(r'''E(X) = \frac{1}{p}''')
    
    st.markdown('Variance for Geometric Distribution:')
    st.latex(r'''Var(X) = \sigma_{X}^2 = \frac{1-p}{p^2}''')
    
    st.markdown('Standard Deviation for Geometric Distribution:')
    st.latex(r'''\sigma_{X}= \frac{\sqrt{1-p}}{p}''')
    
    st.markdown('')

    
    
    
    st.markdown('### Probability Mass Function (PMF)')
    st.markdown('The probability mass function or PMF of the geometric distribution refers to the function which is used to get the individual probability of obtaining a success on the $x^{th}$ trial. The formula is shown below, where $x$ refers to the trial number and $p$ refers to the probability of success (i.e. item drops successfully) on each trial.')

    st.latex(r'''f(x) = P(X = x) = (1 - p)^{x-1} \times p''')
    
    st.markdown('$(1 - p)$ here refers to the chance of failure on each trial. Therefore, the probability of obtaining the first success on trial number $x$ is for the first $(x - 1)$ trials to be failures, followed by a success. We can do this by multiplying the chance of failure $(x - 1)$ times before multiplying by $p$ for the chance of success on the $x^{th}$ try. We can do this because all all trials are independent of each other, and thus we can get the individual probability of $P(X = x)$ this way.')
    
    
    
    
    st.markdown('### Cumulative Distribution Function (CDF)')
    st.markdown('The cumulative distribution function or CDF of the geometric distribution refers to the function which is used to get the **cumulative probability** of obtaining a success by the $x^{th}$ trial. The mathematical formula for this is again shown below, where $x$ refers to the trial number and $p$ refers to the probability of success (i.e. item drops successfully) on each trial.')
    
    st.latex(r'''F(x) = P(X \le x) = 1 - (1 - p)^x''')
    
    st.markdown('To find the cumulative probabilities of item drops at or before the $x^{th}$ trial, we can use the basic probability rule of [**complements**](https://www.ck12.org/book/ck-12-advanced-probability-and-statistics-concepts/section/3.3/):')
    
    st.latex(r'''P(X \le x) = 1 - P(X > x)''')
    
    st.markdown('In this case, $P(X > x)$ can be written as the probability that the first $x$ trials are failures. Since we have established that $(1 - p)$ is the chance of failure, we can simply obtain $P(X > x)$ by mutliplying $(1 - p)$ by itself $x$ number of times to obtain the total probability that the first $x$ trials are failures. After that, we can easily obtain $P(X \le x)$ by subtracting $P(X > x)$ from $1$ to get the cumulative probability of $F(x)$.')
    
    
    
    
    st.markdown('### Conclusion')
    st.markdown('These two functions were used to plot the graphs and calculations on the main page, with the first graph (in blue) showing the PMF of drop rates and the second (in red) showing the CDF of drop rates. Note that the PMF of drop rates actually decreases the more the number of trials increases, indicating that it is extremely unlikely that players will need to farm more than the expected number of times to get their item drop. **Think about it this way**: You flip a coin multiple times. What is the chance that you will get your first head only on the 36th flip? Pretty unlikely, right? The same logic applies here. Even if item drop rates are very low, the geometric distribution actually proves that you are **more likely** to get a rare drop after farming for some time than not getting a rare drop. Keep this in mind the next time you feel like complaining about the drop rates in the game!')

    st.markdown("**Read more at**: &nbsp;&nbsp;&nbsp;[**Statistics How To - Geometric Distribution**](https://www.statisticshowto.com/geometric-distribution/)")
    st.markdown('---')
    st.markdown('*This web app is in no way affiliated with AdventureQuest Worlds or Artix Entertainment.*')

    
    
    
if __name__ == "__main__":
    main()
