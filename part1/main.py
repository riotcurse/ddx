from fastapi import FastAPI,Depends

#custom error just because
class DataInterfaceException(Exception):
    pass 

#parent class for pretending there's a service layer on top of the
#test json, mostly just to keep my brain organized
class DataInterface():
    def __init__(self,json_data: dict):
        self.jd = json_data

    def known_noun(self,name: str, all_names: list,noun: str):
        if name not in all_names:
            message = f"{name} is not a {noun}."
            raise DataInterfaceException(message)


#would probably want to use one of the five billion json query language 
#libraries available for python out there instead of doing all of this
#whole cloth

#i'm also assuming that the json structure we're working with is identical
#to the one presented in the pdf. I'd rather make this more flexible, 
#but i'm trying to finish the rough draft before I start the next one

class JsonDataInterface_primaries(DataInterface):

    def get_state_names(self):
        return [key for key in self.jd]

    def get_state_data(self,state_name: str):
        all_states = self.get_state_names()

        self.known_noun(state_name,all_states,"state")

        return self.jd[state_name]

    def get_county_names(self,state_name: str):
        state_data = self.get_state_data(state_name)

        return [key for key in state_data]

    def get_county_data(self,state_name: str,county_name: str):
        all_counties = self.get_county_names(state_name)

        noun = f"county in {state_name}"
        self.known_noun(county_name,all_counties,noun)
        
        return self.jd[state_name][county_name]

    def get_party_names(self,state_name: str,county_name: str):
        county_data = self.get_county_data(state_name,county_name)

        return [key for key in county_data]

    def get_party_data(self, state_name: str, county_name: str, party_name: str):

        all_parties = self.get_party_names(state_name,county_name)
        
        noun = f"party represented in {county_name}, {state_name}."
        self.known_noun(party_name,all_parties,noun)

        return self.jd[state_name][county_name][party_name]

    #skipping a step in the pattern here
    def get_all_candidates(self, state_name: str, county_name: str, party_name: str):
        party_data = self.get_party_data(state_name,county_name,party_name)

        result = [{"name":k,"votes":v} for k,v in party_data.items()]

        return result 

    #might want to break everything below here into a separate object 
    #for business logic
    #but time is of the essence here

    def find_winner(self,candidate_list:list):

        if not candidate_list or len(candidate_list) == 0:
            raise DataInterfaceException("No candidates provided")

        winner = candidate_list[0]
        
        if len(candidate_list) > 1:

            for c in candidate_list[1:]:
                if c["votes"] > winner["votes"]:
                    winner = c

        return winner 

    #this could be way better
    #okay I looked it up and there are actually only a little over 3,000 counties and county-esqueentities in the US
    #so this probably wouldn't be the worst
    def do_the_thing(self):
        result = []
        for state in self.get_state_names():
            for county in self.get_county_names(state):
                for party in self.get_party_names(state,county):
                    candidates = self.get_all_candidates(state,county,party)
                    winner = self.find_winner(candidates)
                    row = {"state":state,"county":county,"party":party,"name":winner["name"],"votes":winner["votes"]}
                    result.append(row)

        return result


#test data
test_data = {
    "Pennsylvania":{
        "Chester":{
            "Democrats":{
                "Humphrey":10000,
                "McGovern":5000
            },
            "Republicans":{
                "Nixon":20000,
                "Ashbrook":200,
                "McCloskey":100
            }
        }
    },
    "New York":{
        "RoChester":{
            "Democrats":{
                "Humphrey":10001,
                "McGovern":5001
            },
            "Republicans":{
                "Nixon":20001,
                "Ashbrook":201,
                "McCloskey":101
            }
        }
    }
}


#dependency function for fast api route
def get_pseudo_db():
    return JsonDataInterface_primaries(test_data)


#api here
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, DDx"}

@app.get("/countywinners")
async def winners(pseudo_db = Depends(get_pseudo_db)):
    return pseudo_db.do_the_thing()




##TODO
# 1) split everything out into modules/a proper project structure
# 2) unit test everything
# 3) document everything more professionally
# 4) package the api properly
# 5) code review by peers

##NEXT STEPS
# Add routes to allow querying of results by state, county, candidate name, etc
# Add auth
# Serve the data out of a database
# Make openapi compliant
# ???
# Profit
