import csv


results = []
with open('tradingData180320.csv') as File:
    reader = csv.reader(File)
    results = list(reader)


def main():
    i = 1
    dictionary_users = {}
    #j = 0
    while i < len(results):
        newList = []
        dictionary_users[results[i][0]] = newList
        i = i + 1
        #j = j + 1

    count = 0
    user_information_list = {}
    user_stock_list = {}
    for x in dictionary_users.keys():
        j = 1
        userList = []
        while j < len(results):
            if(x == results[j][0]):
                userList.append(results[j])
            j = j + 1
        dictionary_users[x] = userList
    with open('user_holdings.csv', 'w') as csvfile:
        fieldnames = ['UserID', 'Employment Status', 'Employment Position', 'Employment Business', 'YOB', 'Gender', 'Postcode', 'Suburb', 'State', 'Ticker', 'USD Holdings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for y in dictionary_users.keys():

            userList = dictionary_users[y]
            ticker_count_for_user = {}
            for z in userList:
                ticker = z[3]
                if (ticker not in ticker_count_for_user):
                    if (z[7] == 'B'):
                        ticker_count_for_user[ticker] = float(z[9])
                    else:
                        ticker_count_for_user[ticker] = -float(z[9])

                else:
                    if (z[7] == 'B'):
                        ticker_count_for_user[ticker] += float(z[9])
                    else:
                        ticker_count_for_user[ticker] -= float(z[9])

            new_user_list_keys = {}

            for t in ticker_count_for_user.keys():
                if ticker_count_for_user[t] > 0:
                    new_user_list_keys[t] = ticker_count_for_user[t];

            user_stock_list[y] = new_user_list_keys
            user_information = []

            user_information.append(userList[0][0])
            user_information.append(userList[0][10])
            user_information.append(userList[0][11])
            user_information.append(userList[0][12])
            try:
                user_information.append((userList[0][13])[len(int(userList[0][13])-2):len(int(userList[0][13])-1)])
            except:
                user_information.append('NA')
            user_information.append(userList[0][14])
            user_information.append(userList[0][15])
            user_information.append(userList[0][16])
            user_information.append(userList[0][17])

            user_information_list[y] = user_information

            for k in new_user_list_keys.keys():
                writer.writerow({'UserID': user_information[0],
                'Employment Status': user_information[1], 'Employment Position': user_information[2],
                'Employment Business': user_information[3], 'YOB': user_information[4],
                'Gender': user_information[5], 'Postcode': user_information[6], 'Suburb': user_information[7],
                'State': user_information[8], 'Ticker': k, 'USD Holdings': new_user_list_keys[k]})

    list_subfields = ['UserID', 'Employment_Status', 'Employment_Position', 'Employment_business',
                    'YOB', 'Gender', 'Postcode', 'Suburb', 'State',]
    for g in range (0,9):

        with open('user_holdings_state.'+list_subfields[g] + '.csv', 'w') as csvfile:
            fieldnames = [list_subfields[g],'Ticker', 'USD Holdings']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            ticker_and_values= {}
            list_states = {}


            for user_id in user_information_list.keys():
                list_stocks_user = user_stock_list[user_id]

                for stock in list_stocks_user.keys():
                    if user_information_list[user_id][g] not in list_states:
                        list_tickers = {}
                        list_tickers[stock] = list_stocks_user[stock]
                        list_states[user_information_list[user_id][g]] = list_tickers
                    else:
                        current_state_list_dict = list_states[user_information_list[user_id][g]]
                        if stock not in current_state_list_dict:
                            current_state_list_dict[stock] = list_stocks_user[stock]
                        else:
                            current_state_list_dict[stock] += list_stocks_user[stock]

            for state in list_states.keys():
                    stock_list = list_states[state]
                    for stock in stock_list.keys():
                        writer.writerow({list_subfields[g]: state, 'Ticker': stock, 'USD Holdings':stock_list[stock]})


        #for z in ticker_count_for_user.keys():
        #    if (ticker_count_for_user[z] > 1):


        #print("user: " + str(x) + "list: " + str(dictionary_users[y]))
        #print("ticker dictionary:" + str(ticker_count_for_user))
        #print(count)
        #count = count + 1

main()
