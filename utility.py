import pandas as pd


def read_data(filename):
    """
    Reads an excel file with given filename
    :param filename:
    :return: pandas.DataFrame from the excel file
    """
    assert isinstance(filename, str)
    return pd.read_excel(filename)


def find_average_col(df, col):
    """
    calculates the mean of the given column from input dataframe file
    :param df: datafile
    :param col: column name
    :return: average value of the selected column
    """
    assert isinstance(df, pd.DataFrame)
    assert col in df.columns
    return df[col].mean()


def plot_overlaid_bar(df1, df2, color1='Blue', color2='Red', alpha=1, kind='barh', title="", ax=None, legend=[],
                      grid=False):
    """

    :param df1:
    :param df2:
    :param color1:
    :param color2:
    :param alpha:
    :param kind:
    :param title:
    :return:
    """
    if ax is None:
        ax = df1.plot(kind=kind, title=title, alpha=alpha, color=color1)
    else:
        df1.plot(kind=kind, title=title, alpha=alpha, color=color1, ax=ax)
    df2.plot(ax=ax, kind=kind, alpha=alpha, color=color2, grid=grid)
    ax.legend(legend)
    ax.set_frame_on(False)
    return ax


# Plotting
if __name__ == "__main__":
    filename = "financial.xlsx"
    financial = read_data(filename)

    ug_loan_avg = find_average_col(financial, 'Undergrad Loan')
    ug_aid_avg = find_average_col(financial, 'Undergrad Aid')
    grad_loan_avg = find_average_col(financial, 'Graduate Loan')
    grad_aid_avg = find_average_col(financial, 'Graduate Aid')

    tuition = pd.read_excel("tuition.xlsx")

    # plot tuition data
    ax = tuition.plot(kind='bar', rot=0, title="Tuition and fees")
    ax.set_xlabel("Years")
    ax.set_ylabel("Dollars ($)")
    # put value labels on bars
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x(), p.get_height() * 1.01))

    # total_fee = tuition.mean() +
    filename = "salary_as.xlsx"
    salary_as = read_data(filename)
    filename = "salary_ug.xlsx"
    salary_ug = read_data(filename)
    filename = "salary_grad.xlsx"
    salary_grad = read_data(filename)
