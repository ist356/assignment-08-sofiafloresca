import pandas as pd
import streamlit as st 


def top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    filtered = violations_df.pivot_table(index='location', values='amount', aggfunc='sum').sort_values(by='amount', ascending=False)
    filtered['location'] = filtered.index
    filtered.reset_index(drop=True, inplace=True)
    return filtered[filtered['amount'] >= threshold]


def top_locations_mappable(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    high_ticket_locations = top_locations(violations_df, threshold)
    locations = violations_df[['location', 'lat', 'lon']].drop_duplicates(subset=['location'])
    merged = pd.merge(high_ticket_locations, locations, on='location').drop_duplicates()
    return merged


def tickets_in_top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    high_ticket_locations = top_locations(violations_df, threshold)
    merged = pd.merge(high_ticket_locations[['location']], violations_df, on='location')
    return merged

if __name__ == '__main__':
    '''
    Main ETL job. 
    '''
    violations = pd.read_csv('./cache/final_cuse_parking_violations.csv')
    locations = top_locations(violations)
    locations.to_csv('./cache/top_locations.csv', index=False)
    mappable = top_locations_mappable(violations)
    mappable.to_csv('./cache/top_locations_mappable.csv', index=False)
    tickets = tickets_in_top_locations(violations)
    tickets.to_csv('./cache/tickets_in_top_locations.csv', index=False)