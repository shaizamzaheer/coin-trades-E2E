from searchtweets import load_credentials

load_credentials(filename="./search_tweets_creds_example.yaml",
                 yaml_key="search_tweets_v2_example",
                 env_overwrite=False)

from searchtweets import ResultStream, gen_request_parameters

if __name__ == "__main__":
    query = gen_request_parameters("snow", results_per_call=100)
    print(query)