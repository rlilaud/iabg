
def intersight_get(resource_path, private_key, 
    public_key, query_params=None):
    # Import "intersight_rest" Package
    import intersight_rest as isREST
    # Import JSON Package
    import json
    import pprint as pp
    # Load Public/Private Keys
    isREST.set_private_key(private_key)
    isREST.set_public_key(public_key)
    #isREST.set_private_key(open(r".\keys\private_key.pem", "r") .read())
    #isREST.set_public_key(open(r".\keys\public_key.txt", "r") .read())
    if query_params!=None:
        options = {
            "http_method": "get",
            "resource_path": resource_path,
            "query_params": query_params
            }
    elif query_params==None:
        options = {
            "http_method": "get",
            "resource_path": resource_path
            }
            
    #-- Send GET Request --#
    results = isREST.intersight_call(**options)
    print("Status Code: " + str(results.status_code))
    #data = json.dumps(results.json())
    #pp.pprint(results.json(), indent=2)
    return results.json()
