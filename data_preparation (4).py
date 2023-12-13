import pandas as pd
import re
#
# 1. Prepare data (apply necessary cleaning, feature encoding, transformations and features)

df_yelp = pd.read_csv('restaurants1/yelp.csv', encoding='utf-8')
df_zomato = pd.read_csv('restaurants1/zomato.csv')

print(f"################################")
print(f"Number of Yelp entries: {df_yelp.shape[0]}")
print(f"Number of Yelp features: {df_yelp.shape[1]}")
print(f"Yelp feature names: {df_yelp.columns.tolist()}")
print(f"################################")
print(f"Number of Zomato entries: {df_zomato.shape[0]}")
print(f"Number of Zomato features: {df_zomato.shape[1]}")
print(f"Zomato feature names: {df_zomato.columns.tolist()}")
print(f"################################")


# trim names of restaurants.
def trim_names(df):
    df['NAME'] = df['NAME'].str.strip()
    print('Trimmed entry names.')
    return df


# if NAME and ADDRESS are the same -> duplicate
def remove_duplicates(df):
    df_removed = df.drop_duplicates(subset=['NAME', 'ADDRESS'], keep='first')
    entries_removed = df.shape[0] - df_removed.shape[0]
    print(f"{entries_removed} duplicate entries removed.")
    return df_removed


# if NAME contains the substring "review of" -> remove it
def remove_reviews(df):
    df_removed = df[~df['NAME'].str.contains("review of")]
    entries_removed = df.shape[0] - df_removed.shape[0]
    print(f'{entries_removed} "review of" entries removed.')
    return df_removed


# replace corrupted symbols with their respective correct character
def replace_special_chars(df):
    df_replaced = df.replace({
        # correct apostrophes
        '\�۪': "'",
        # correct ü
        '\�_': "ü"
    }, regex=True)
    print('Fixed special characters.')
    return df_replaced

# Fix places containing a '-' in their name only contain characters before the '-' sign as name value
def clean_title_with_hyphen(df):
    df['NAME'] = df['NAME'].str.split('-').str[0]
    print('Removed text after the first "-"')
    return df

# Clean names to remove the special characters
def clean_special_characters_from_name(df):
    result_list = []
    pattern = re.compile(r'[^a-zA-Z0-9\s.,!?;:()\'"-]')

    for string in df['NAME']:
        cleaned_string = re.sub(pattern, '', string)
        result_list.append(cleaned_string)
    df['NAME'] = result_list
    return df

# remove all non-numeric characters from phonenumbers (probably not required)
def clean_phone_number(df):
    def format_phone_numbers(phone):
        cleaned_phone = ''.join(c for c in phone if c.isdigit())
        if len(cleaned_phone) == 10:
            return f"({cleaned_phone[:3]}) {cleaned_phone[3:6]}-{cleaned_phone[6:]}"
        return cleaned_phone
    df['PHONENUMBER'] = df['PHONENUMBER'].apply(format_phone_numbers)
    return df


# fix NAN values in ratings
def fix_nan_in_ratings(df):
    mean_rating = df['RATING'].mean()
    df['RATING'] = df.apply(lambda row: 0 if row['NO_OF_REVIEWS'] == 0 else mean_rating if pd.isna(
        row['RATING']) else row['RATING'], axis=1)
    print("Fixed NaN values in the Rating column")
    return df


# remove all entries with '1445980000000' as a phone number.
def remove_incorrect_phone_numbers(df):
    df_removed = df[df['PHONENUMBER'] != '1445980000000']
    entries_removed = df.shape[0] - df_removed.shape[0]
    print(f'{entries_removed} entries with incorrect phone numbers removed.')
    return df_removed


# remove entries with incomplete addresses
def remove_incomplete_address(df):
    mask = df['ADDRESS'].str.count(',') >= 2
    df_removed = df[mask]
    entries_removed = df.shape[0] - df_removed.shape[0]
    print(f'{entries_removed} entries with incorrect address removed.')
    return df_removed


def clean_df(df, output_path):
    df = trim_names(df)
    df = remove_duplicates(df)
    df = remove_reviews(df)
    df = replace_special_chars(df)
    df = clean_title_with_hyphen(df)
    df = clean_special_characters_from_name(df)
    df = clean_phone_number(df)
    df = remove_incorrect_phone_numbers(df)
    df = fix_nan_in_ratings(df)
    df = remove_incomplete_address(df)
    df.to_csv(output_path, encoding='utf-8')

df_yelp_cleaned = df_yelp
df_zomato_cleaned = df_zomato
print("Cleaning the Yelp dataset:")
clean_df(df_yelp_cleaned, 'restaurants1/yelp.cleaned.csv')
print('__________________________________________________________')
print("Cleaning the Zomato dataset:")
clean_df(df_yelp_cleaned, 'restaurants1/zomato.cleaned.csv')
