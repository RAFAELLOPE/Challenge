#from src.challenge import DatasetConsumption
#from src.data_access import DatasetAccess
from src.challenge import DatasetConsumption
import pandas as pd 
import numpy as np 
import scipy.stats
import time

def test_data_consumption():
    """
    To test the data consumer we are going to generate 10.000 samples of a synthetic data with the following data.
    We also generate a small percentage of null values.
    If the percentage of null values is high, one would need to check the process that generated these values (MAR, MCAR,..)

    Probabilities of occurrence of each country:
    SP = Spain           ---> P=10%
    UK = United Kingdom  ---> P=20%
    US = United States   ---> P=30%
    GE = Germany         ---> P=20%
    FR = France          ---> P=10%
    NL = The Netherlands ---> P=9%
    NULL                 ---> P=1%

    Probabilities of occurrence of each status:
    PENDING              ---> P=20%
    COMPLETED            ---> P=50%
    FAIL                 ---> P=30%

    Probability distribution of the amount:
    We generate a random sample of size 2000 from a Normal distribution with: 
        MEAN = 1e6 
        STANDARD DEVIATION = 1e5
    """
    country = np.random.choice(a=['SP', 'UK', 'US', 'GE', 'FR', 'NL', np.nan],
                               size= 10000,
                               p=[0.1, 0.2, 0.3, 0.2, 0.1, 0.09, 0.01])
    
    status = np.random.choice(a=['PENDING', 'COMPLETED', 'FAILED'],
                              size=10000,
                              p=[0.2, 0.5, 0.3])
    
    mean = 1e6
    std = 1e5
    amount = np.random.normal(loc=mean, scale=std, size=10000)
    # We randomly set some null values in the amount with the use of a mask
    mask = np.random.choice(a=[0,1], size=10000, p=[0.05, 0.95])
    amount[mask == 0] = np.nan
    # We simulate the creation of a dataframe from data coming in JSON format 
    # with fields 'id', 'country', 'status', 'amount'.
    # The id is automatically created by the index of the dataframe
    # We assume a call to DatasetAccess to retrieve data in a json (or dict)
    df_test = pd.DataFrame({'country':country, 'status':status, 'amount':amount})
    df_test.replace('nan', np.nan, inplace=True)

    # Create a DatasetConsumption object
    transformer = DatasetConsumption(df_test)
    # Get transformed dataframe and measure time
    start_time = time.time()
    new_df = transformer.get_transformed_dataset()
    print(f" --- time (seconds) -- {time.time() - start_time}")

    #CHECKS
    ###############################################################################
    # Average outstanding = P(country)*P(pending)

    # Average outstanding France FR = P(FR) * P(pending) = 0.1 * 0.2 = 0.02
    # Average outstanding Spain SP = P(SP) * P(pending) = 0.1 * 0.2 = 0.02
    # Average outstanding United Kingdom = P(UK) * P(pending) = 0.2 * 0.2 = 0.04
    # Average outstanding United States = P(US) * P(pending) = 0.3 * 0.2 = 0.06
    # Average outstanding Germany = P(GE) * P(pending) = 0.2 * 0.02 = 0.04
    # Average outstanding The Netherlands = P(NL) * P(pending) = 0.09 * 0.2 = 0.018
    # ** Assume numeric error of 0.005 for simplicyty but this should be carefully computed **
    epsilon = 0.005
    assert abs(new_df[new_df['country'] == 'FR']['average_outstanding'].values[0] - 0.02) <= epsilon
    assert abs(new_df[new_df['country'] == 'SP']['average_outstanding'].values[0] - 0.02) <= epsilon
    assert abs(new_df[new_df['country'] == 'UK']['average_outstanding'].values[0] - 0.04) <= epsilon
    assert abs(new_df[new_df['country'] == 'US']['average_outstanding'].values[0] - 0.06) <= epsilon
    assert abs(new_df[new_df['country'] == 'GE']['average_outstanding'].values[0] - 0.04) <= epsilon
    assert abs(new_df[new_df['country'] == 'NL']['average_outstanding'].values[0] - 0.018) <= epsilon

    # Amounts has been generated from a normal distribution centered at 1M.

    # This distribution is symmetric, therefore 0.5 probability of getting an amount > 1M
    # and 0.5 probability of getting an amount < 0.5.
    # We consider 6 groups:
    #     1- Country FR and status FAILED
    #     2- Country SP and status FAILED
    #     3- Country UK and status FAILED
    #     4- Country US and status FAILED
    #     5- Country GE and status FAILED
    #     6- Country NL and status FAILED

    # If we had an infinite number of samples in each group, we would compute an exact mean value (1M)
    # and the probability of getting a value less or equal (or greater than) to the mean would be 0.5.
    # In this case, the probability of crital rate per country is computed as:
    # Critical rate = P(country) * P(amount > 1M) * P(failed) = P(country) * 0.5 * P(failed)

    # Nevetheless we have a finite number of samples in each group so, the mean computed in each group 
    # will have an error. Hence the probabilities of getting a value less or equal (or greater than) the mean would vary from 0.5
    # The standard error (se) in each group depends on the number of samples N_country in each group.

    df_fr = df_test[(df_test['country'] == 'FR') & (df_test['status'] == 'FAILED')]
    df_sp = df_test[(df_test['country'] == 'SP') & (df_test['status'] == 'FAILED')]
    df_uk = df_test[(df_test['country'] == 'UK') & (df_test['status'] == 'FAILED')]
    df_us = df_test[(df_test['country'] == 'US') & (df_test['status'] == 'FAILED')]
    df_ge = df_test[(df_test['country'] == 'GE') & (df_test['status'] == 'FAILED')]
    df_nl = df_test[(df_test['country'] == 'NL') & (df_test['status'] == 'FAILED')]

    N_fr = len(df_fr)
    N_sp = len(df_sp)
    N_uk = len(df_uk)
    N_us = len(df_us)
    N_ge = len(df_ge)
    N_nl = len(df_nl)

    # The standard error is computed as the standard deviation divided by the squared-root of the number of samples.

    se_fr = np.std(df_fr)/np.sqrt(N_fr)
    se_sp = np.std(df_sp)/np.sqrt(N_sp)
    se_uk = np.std(df_uk)/np.sqrt(N_uk)
    se_us = np.std(df_us)/np.sqrt(N_us)
    se_ge = np.std(df_ge)/np.sqrt(N_ge)
    se_nl = np.std(df_nl)/np.sqrt(N_nl)

    # From this standard error, we compute a minimum and maximum probabilities of getting a value lower than (greater than) the 
    # mean +- standard error

    p_max_fr = scipy.stats.norm(mean, std).cdf(mean + se_fr[0])
    p_min_fr = scipy.stats.norm(mean, std).cdf(mean - se_fr[0])
    p_max_sp = scipy.stats.norm(mean, std).cdf(mean + se_sp[0])
    p_min_sp = scipy.stats.norm(mean, std).cdf(mean - se_sp[0])
    p_max_uk = scipy.stats.norm(mean, std).cdf(mean + se_uk[0])
    p_min_uk = scipy.stats.norm(mean, std).cdf(mean - se_uk[0])
    p_max_us = scipy.stats.norm(mean, std).cdf(mean + se_us[0])
    p_min_us = scipy.stats.norm(mean, std).cdf(mean - se_us[0])
    p_max_ge = scipy.stats.norm(mean, std).cdf(mean + se_ge[0])
    p_min_ge = scipy.stats.norm(mean, std).cdf(mean - se_ge[0])
    p_max_nl = scipy.stats.norm(mean, std).cdf(mean + se_nl[0])
    p_min_nl = scipy.stats.norm(mean, std).cdf(mean - se_nl[0])

    # This way, the crital rate must lie between [P(country) * P(amount > 1M - se) * P(failed)] and [P(country) * P(amount <= 1M + se) * P(failed)]
    # In addition, we assume a numeric error.
    
    critical_rate_fr = new_df[new_df['country'] == 'FR']['critical_rate'].values[0]
    critical_rate_sp = new_df[new_df['country'] == 'SP']['critical_rate'].values[0]
    critical_rate_uk = new_df[new_df['country'] == 'UK']['critical_rate'].values[0]
    critical_rate_us = new_df[new_df['country'] == 'US']['critical_rate'].values[0]
    critical_rate_ge = new_df[new_df['country'] == 'GE']['critical_rate'].values[0]
    critical_rate_nl = new_df[new_df['country'] == 'NL']['critical_rate'].values[0]


    assert (critical_rate_fr <= 0.1*p_max_fr*0.3 + epsilon) and (critical_rate_fr > 0.1*p_min_fr*0.3 - epsilon), "Check critical rate computed for FR"
    assert (critical_rate_sp <= 0.1*p_max_sp*0.3 + epsilon) and (critical_rate_sp > 0.1*p_min_sp*0.3 - epsilon), "Check critical rate computed for SP"
    assert (critical_rate_uk <= 0.2*p_max_uk*0.3 + epsilon) and (critical_rate_uk > 0.2*p_min_uk*0.3 - epsilon), "Check critical rate computed for UK"
    assert (critical_rate_us <= 0.3*p_max_us*0.3 + epsilon) and (critical_rate_us > 0.3*p_min_us*0.3 - epsilon), "Check critical rate computed for US"
    assert (critical_rate_ge <= 0.2*p_max_ge*0.3 + epsilon) and (critical_rate_ge > 0.2*p_min_ge*0.3 - epsilon), "Check critical rate computed for GE"
    assert (critical_rate_nl <= 0.09*p_max_nl*0.3 + epsilon) and (critical_rate_nl > 0.09*p_min_nl*0.3 - epsilon), "Check critical rate computed for NL"

    # By simmetry of the normal distribution, we compute can check the error rate in the same way
    error_rate_fr = new_df[new_df['country'] == 'FR']['error_rate'].values[0]
    error_rate_sp = new_df[new_df['country'] == 'SP']['error_rate'].values[0]
    error_rate_uk = new_df[new_df['country'] == 'UK']['error_rate'].values[0]
    error_rate_us = new_df[new_df['country'] == 'US']['error_rate'].values[0]
    error_rate_ge = new_df[new_df['country'] == 'GE']['error_rate'].values[0]
    error_rate_nl = new_df[new_df['country'] == 'NL']['error_rate'].values[0]

    assert (error_rate_fr <= 0.1*p_max_fr*0.3 + epsilon) and (error_rate_fr > 0.1*p_min_fr*0.3 - epsilon), "Check error rate computed for FR"
    assert (error_rate_sp <= 0.1*p_max_sp*0.3 + epsilon) and (error_rate_sp > 0.1*p_min_sp*0.3 - epsilon), "Check error rate computed for SP"
    assert (error_rate_uk <= 0.2*p_max_uk*0.3 + epsilon) and (error_rate_uk > 0.2*p_min_uk*0.3 - epsilon), "Check error rate computed for UK"
    assert (error_rate_us <= 0.3*p_max_us*0.3 + epsilon) and (error_rate_us > 0.3*p_min_us*0.3 - epsilon), "Check error rate computed for US"
    assert (error_rate_ge <= 0.2*p_max_ge*0.3 + epsilon) and (error_rate_ge > 0.2*p_min_ge*0.3 - epsilon), "Check error rate computed for GE"
    assert (error_rate_nl <= 0.09*p_max_nl*0.3 + epsilon) and (error_rate_nl > 0.09*p_min_nl*0.3 - epsilon), "Check error rate computed for NL"
