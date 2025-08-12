import requests

def factorize(n):
    try:
        print(f"\nFactoring {n} using FactorDB...")
        response = requests.get(f"http://factordb.com/api", params={"query": str(n)})
        response.raise_for_status()
        data = response.json()
        
        if "factors" in data:
            factors = data["factors"]
            print("\nFactors Found:")
            for factor, count in factors:
                print(f"Factor: {factor}, Count: {count}")
            return factors, None
        else:
            print("Unable to find factors for the given number.")
            return None, "Unable to find factors for the given number."
    except requests.RequestException as e:
        print(f"Error querying FactorDB: {e}")
        return None, f"Error querying FactorDB: {e}"
