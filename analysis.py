import pandas as pd
import matplotlib

from utility import *


def plot_tuition_by_year(tuition_fname="dataset/tuition.xlsx"):
    """
    reads tuition data and plot the yearly tuition data
    :param tuition_fname: input filename
    :return:matplotlib axes plot
    """

    tuition = read_data(tuition_fname)

    color = ["CornflowerBlue", "Tomato", "Blue", "Red", "black"]
    # plot tuition data
    ax = tuition.plot(kind='bar', rot=0, title="Tuition and fees", color=color)
    ax.set_xlabel("Years")
    ax.set_ylabel("Dollars ($)")
    ax.set_frame_on(False)
    ax.legend(bbox_to_anchor=(1, 1))

    return ax


def plot_tuition_average(tuition_fname="dataset/tuition.xlsx"):
    """
    plot the averaged tuition data
    :param tuition_fname:
    :return:matplotlib axes plot
    """

    tuition = read_data(tuition_fname)
    total_with_room = pd.DataFrame(tuition.mean()[0:4] + find_average_col(tuition, "Room and Board")).astype(int)
    total = pd.DataFrame(tuition.mean()[0:4]).astype(int)

    ax = total_with_room.plot(kind="barh", title="Averaged tuition cost with Room & Board",
                              alpha=1, color="Tomato")
    # set individual bar lables using above list
    for i in ax.patches:
        # get_width pulls left or right; get_y pushes up or down
        ax.text(i.get_width() + 500, i.get_y() + i.get_height() / 3,
                "$" + str(i.get_width()), fontsize=13,
                color='black')

    total.plot(ax=ax, kind="barh", alpha=1, color="CornflowerBlue")
    ax.set_frame_on(False)
    ax.set_xlim([0, 50000])
    ax.legend(["Room & Board", "Tuition & Fees"], bbox_to_anchor=(1, 1))

    return ax


def plot_financial(financial_fname="dataset/financial.xlsx"):
    """
    plots financial data
    :param financial_fname:
    :return:matplotlib axes plot
    """
    financial = read_data(financial_fname)

    year = [2015, 2016, 2017, 2018]
    color = ["CornflowerBlue", "Tomato", "Blue", "Red", "black"]
    ax = financial.plot(kind='line', rot=0, title="Financial Aids and Loans",
                        linestyle='-', marker='o', color=color)
    ax.set_xlabel("Years")
    ax.set_ylabel("Dollars ($)")
    ax.set_xticks(year)
    ax.set_frame_on(False)
    ax.legend(bbox_to_anchor=(1, 1))

    return ax


def calculate_fee_with_aids(tuition_fname="dataset/tuition.xlsx", financial_fname="dataset/financial.xlsx"):
    """
    calculates averaged fees with financial aids
    :param tuition_fname:
    :param financial_fname:
    :return: total_fee, total_fee_with_aid, ug_aid_avg, grad_aid_avg
    """
    financial = read_data(financial_fname)
    tuition = read_data(tuition_fname)

    # calculate averaged total fees
    total_fee = pd.DataFrame(tuition.mean()[0:4] + find_average_col(tuition, "Room and Board")).astype(int)

    ug_loan_avg = find_average_col(financial, 'Undergrad Loan')
    ug_aid_avg = find_average_col(financial, 'Undergrad Aid')
    grad_loan_avg = find_average_col(financial, 'Graduate Loan')
    grad_aid_avg = find_average_col(financial, 'Graduate Aid')

    ug_total_fee_with_aid = total_fee[0:2] - ug_aid_avg
    grad_total_fee_with_aid = total_fee[2:4] - grad_aid_avg
    total_fee_with_aid = pd.concat((ug_total_fee_with_aid, grad_total_fee_with_aid)).astype(int)

    return total_fee, total_fee_with_aid, ug_aid_avg, grad_aid_avg


def plot_cost_with_aid(tuition_fname="dataset/tuition.xlsx", financial_fname="dataset/financial.xlsx"):
    """
    plots tuitions costs after financial aids
    :param tuition_fname:
    :param financial_fname:
    :return:matplotlib axes plot
    """

    total_fee, total_fee_with_aid, ug_aid_avg, grad_aid_avg = calculate_fee_with_aids()

    ax = total_fee_with_aid.plot(kind="barh", alpha=1, color="CornflowerBlue")

    # set individual bar lables using above list
    for i in ax.patches:
        # get_width pulls left or right; get_y pushes up or down
        ax.text(i.get_width() + 500, i.get_y() + i.get_height() / 3,
                "$" + str(i.get_width()), fontsize=13,
                color='black')
    total_fee.plot(kind="barh", title="Averaged Cost with Financial Aids",
                   alpha=0.3, color="gray", ax=ax)

    ax.set_frame_on(False)
    ax.set_xlim([0, 50000])
    ax.legend(["With Financial Aids", "Difference"], bbox_to_anchor=(1, 1))

    return ax

def plot_salary():
    """
    plots averaged salary data 
    :return:matplotlib axes plot
    """
    salary_as, salary_ug, salary_grad, \
    salary_as_mean_all, salary_ug_mean_all, salary_grad_mean_all, \
    salary_ug_max, salary_grad_max, salary_ug_min, salary_grad_min = calculate_salary_stat()

    difference = (salary_grad.mean() - salary_ug.mean()) / salary_ug.mean()

    ax = plot_overlaid_bar(salary_grad.mean(), salary_ug.mean(),
                           color1="Tomato", color2="CornflowerBlue", alpha=1,
                           title="Averaged Starting Salary ($)", legend=["Master's", "Bachelor's"])

    ax.set_frame_on(False)
    ax.legend(["Master's", "Bachelor's"], bbox_to_anchor=(1, 1))

    # write the difference% next to bars
    for i in range(10):
        num = difference[i] * 100
        patch = ax.patches[i]
        ax.text(patch.get_width() + 500, patch.get_y() + patch.get_height() / 3,
                f"+{num:.1f}%", fontsize=10,
                color='black')
    ax.set_xlim([0, 90000])

    salary_as.mean().plot(ax=ax, kind='barh', color='DarkSlateGray')

    ax.legend(["Master's", "Bachelor's", "Associate's"], bbox_to_anchor=(1, 1))
    return ax


def calculate_salary_stat(salary_fname=["dataset/salary_as.xlsx", "dataset/salary_ug.xlsx", "dataset/salary_grad.xlsx"]):
    """
    calculate stats with salary data
    :param salary_fname:
    :return:
    """
    salary_as = read_data(salary_fname[0])
    salary_ug = read_data(salary_fname[1])
    salary_grad = read_data(salary_fname[2])

    salary_as_mean_all = int(salary_as.mean().mean())  # averaged salary for associates degree
    salary_ug_mean_all = int(salary_ug.mean().mean())  # averaged salary for bachelors degree
    salary_grad_mean_all = int(salary_grad.mean().mean())  # averaged salary for masters degree

    salary_ug_max = int(salary_ug.mean().max().mean())  # max salary for bachelors degree
    salary_grad_max = int(salary_grad.mean().max().mean())  # max salary for masters degree

    salary_ug_min = int(salary_ug.mean().min().mean())  # min salary for bachelors degree
    salary_grad_min = int(salary_grad.mean().min().mean())  # min salary for masters degree

    return salary_as, salary_ug, salary_grad, \
           salary_as_mean_all, salary_ug_mean_all, salary_grad_mean_all, \
           salary_ug_max, salary_grad_max, salary_ug_min, salary_grad_min


def plot_salary_range():
    """
    plots range of starting salary
    :return:matplotlib axes plot
    """
    salary_as, salary_ug, salary_grad, \
    salary_as_mean_all, salary_ug_mean_all, salary_grad_mean_all, \
    salary_ug_max, salary_grad_max, salary_ug_min, salary_grad_min = calculate_salary_stat()

    salary_as_min = int(salary_as.mean().min().mean())
    salary_as_max = int(salary_as.mean().max().mean())

    d = {'Associate\'s': [salary_as_min, salary_as_mean_all, salary_as_max],
         'Bachelor\'s': [salary_ug_min, salary_ug_mean_all, salary_ug_max],
         'Master\'s': [salary_grad_min, salary_grad_mean_all, salary_grad_max]}
    df = pd.DataFrame(data=d)
    ax = df.plot(kind='box', title="Range of Starting Salary")
    ax.set_frame_on(False)
    ax.set_ylim([30000, 90000])
    return ax


def calculate_ug_total():
    """
    calculates the total cost for ug with opportunity cost
    :return:cost_ug_tuition, cost_ug_total
    """
    salary_as, salary_ug, salary_grad, \
    salary_as_mean_all, salary_ug_mean_all, salary_grad_mean_all, \
    salary_ug_max, salary_grad_max, salary_ug_min, salary_grad_min = calculate_salary_stat()

    total_fee, total_fee_with_aid, ug_aid_avg, grad_aid_avg = calculate_fee_with_aids()

    ug_total_fee_with_aid = total_fee[0:2] - ug_aid_avg
    cost_ug_tuition = 4 * ug_total_fee_with_aid
    cost_ug_total = cost_ug_tuition + 2 * salary_as_mean_all

    return cost_ug_tuition, cost_ug_total


def plot_ug_total():
    """
    plots the total cost for ug with opportunity cost
    :param salary_fname:
    :return:matplotlib axes plot
    """

    cost_ug_tuition, cost_ug_total = calculate_ug_total()

    cost_ug_tuition = cost_ug_tuition.T
    cost_ug_tuition.rename(columns={"Undergrad Private": "Private", "Undergrad Public": "Public"}, inplace=True)
    cost_ug_tuition = cost_ug_tuition.T

    cost_ug_total = cost_ug_total.T
    cost_ug_total.rename(columns={"Undergrad Private": "Private", "Undergrad Public": "Public"}, inplace=True)
    cost_ug_total = cost_ug_total.T

    ax = cost_ug_total.plot(kind="barh", alpha=1, color="Tomato")

    # set individual bar lables using above list
    for i in ax.patches:
        # get_width pulls left or right; get_y pushes up or down
        ax.text(i.get_width() + 5000, i.get_y() + i.get_height() / 3,
                "$" + str(int(i.get_width())), fontsize=13,
                color='black')

    cost_ug_tuition.plot(kind="barh", title="Total Cost of Bechelor's with Opporunity Cost",
                         alpha=1, color="CornflowerBlue", ax=ax)

    ax.set_frame_on(False)
    ax.set_xlim([0, 250000])
    ax.legend(["Opportunity Cost", "Tuition & Fee"], bbox_to_anchor=(1, 1))

    return ax


def calculate_grad_total():
    """
    calculates the total cost for grad with opportunity cost
    :return:cost_ug_total, cost_grad_tuition, cost_grad_with_ug, cost_grad_total
    """
    salary_as, salary_ug, salary_grad, \
    salary_as_mean_all, salary_ug_mean_all, salary_grad_mean_all, \
    salary_ug_max, salary_grad_max, salary_ug_min, salary_grad_min = calculate_salary_stat()

    total_fee, total_fee_with_aid, ug_aid_avg, grad_aid_avg = calculate_fee_with_aids()

    cost_ug_tuition, cost_ug_total = calculate_ug_total()

    cost_grad_tuition = 2 * total_fee_with_aid[2:4]  # grad tuition

    cost_grad_with_ug = pd.DataFrame.copy(cost_grad_tuition)
    cost_grad_with_ug[0][0] += cost_ug_total[0][0]  # grad tuition + ug total cost
    cost_grad_with_ug[0][1] += cost_ug_total[0][1]

    cost_grad_total = cost_grad_with_ug + 2 * salary_ug_mean_all  # add opportunity cost

    return cost_ug_total, cost_grad_tuition, cost_grad_with_ug, cost_grad_total


def plot_grad_total():
    """
    plots the total cost for grad with opportunity cost
    :return:matplotlib axes plot
    """

    cost_ug_total, cost_grad_tuition, cost_grad_with_ug, cost_grad_total = calculate_grad_total()

    cost_ug_total = cost_ug_total.T
    cost_ug_total.rename(columns={"Undergrad Private": "Private", "Undergrad Public": "Public"}, inplace=True)
    cost_ug_total = cost_ug_total.T

    cost_grad_with_ug = cost_grad_with_ug.T
    cost_grad_with_ug.rename(columns={"Graduate Private": "Private", "Graduate Public": "Public"}, inplace=True)
    cost_grad_with_ug = cost_grad_with_ug.T

    cost_grad_total = cost_grad_total.T
    cost_grad_total.rename(columns={"Graduate Private": "Private", "Graduate Public": "Public"}, inplace=True)
    cost_grad_total = cost_grad_total.T

    ax = cost_grad_total.plot(kind="barh", alpha=1, color="Tomato")

    # set individual bar lables using above list
    for i in ax.patches:
        # get_width pulls left or right; get_y pushes up or down
        ax.text(i.get_width() + 10000, i.get_y() + i.get_height() / 3,
                "$" + str(int(i.get_width())), fontsize=13,
                color='black')

    cost_grad_with_ug.plot(kind="barh", title="Total Cost of Master's with Opporunity Cost",
                           alpha=1, color="CornflowerBlue", ax=ax)

    cost_ug_total.plot(kind="barh",
                       alpha=1, color="Gray", ax=ax)
    ax.set_frame_on(False)
    ax.set_xlim([0, 400000])
    ax.legend(["Opportunity Cost", "Tuition & Fee", "Bachelor's"], bbox_to_anchor=(1, 1.1))

    return ax


def calculate_years_to_even():
    """
    calculates the years it takes to even the cost with salary data
    :return: years 
    """

    cost_ug_total, cost_grad_tuition, cost_grad_with_ug, cost_grad_total = calculate_grad_total()

    salary_as, salary_ug, salary_grad, \
    salary_as_mean_all, salary_ug_mean_all, salary_grad_mean_all, \
    salary_ug_max, salary_grad_max, salary_ug_min, salary_grad_min = calculate_salary_stat()

    years = pd.concat((cost_ug_total / salary_ug_mean_all, cost_grad_total / salary_grad_mean_all))

    return years


def plot_years_to_even():
    """
    plots years it takes to even the cost
    :return:matplotlib axes plot
    """
    years = calculate_years_to_even()

    color = ["CornflowerBlue", "Tomato", "Blue", "Red"]
    ax = years.plot(kind='barh', color=color, title="# of Years to Even Tuition & Opportunity Cost",
                    legend=False)

    # set individual bar lables using above list
    for i in ax.patches:
        # get_width pulls left or right; get_y pushes up or down
        ax.text(i.get_width() + 0.2, i.get_y() + i.get_height() / 3,
                f"{i.get_width():.1f} Years", fontsize=10,
                color='black')

    ax.set_frame_on(False)

    return ax


def plot_salary_five_years():
    """
    plots the 5 year salary amount versus total tuition cost
    :return:matplotlib axes plot
    """

    salary_as, salary_ug, salary_grad, \
    salary_as_mean_all, salary_ug_mean_all, salary_grad_mean_all, \
    salary_ug_max, salary_grad_max, salary_ug_min, salary_grad_min = calculate_salary_stat()

    cost_ug_tuition, cost_ug_total = calculate_ug_total()
    cost_ug_total, cost_grad_tuition, cost_grad_with_ug, cost_grad_total = calculate_grad_total()

    cost_ug_tuition = cost_ug_tuition.T
    salary_five_year = salary_ug_mean_all * 5
    cost_ug_tuition = cost_ug_tuition.append(
        pd.DataFrame([[salary_five_year, salary_five_year]], columns=list(cost_ug_tuition.columns.values)),
        ignore_index=True)

    cost_grad_tuition = cost_grad_tuition.T
    salary_five_year = salary_grad_mean_all * 5
    cost_grad_tuition = cost_grad_tuition.append(
        pd.DataFrame([[salary_five_year, salary_five_year]], columns=list(cost_grad_tuition.columns.values)),
        ignore_index=True)
    cost_grad_tuition

    salary_five_years_versus_tuition = pd.concat((cost_ug_tuition, cost_grad_tuition), axis=1).astype(int)

    ax = salary_five_years_versus_tuition.T.plot(kind='barh', title="Salary over 5 Years vs. Tuition & Fees")
    ax.set_frame_on(False)
    ax.set_xlim([0, 350000])
    ax.legend(["Tuition & Fee", "Salary over 5 Years"], bbox_to_anchor=(1, 1))
    return ax


if __name__ == "__main__":
    plot_tuition_by_year()
    plot_tuition_average()
    plot_financial()
    plot_cost_with_aid()
    plot_salary()
    plot_salary_range()
    plot_ug_total()
    plot_grad_total()
    plot_years_to_even()
    plot_salary_five_years()