
with county_highest_votes as (
    SELECT 
        MAX(votes) votes,
        state,
        county,
        party
    FROM results
    GROUP BY state,county,party
)

SELECT 
    r.state,
    r.county,
    r.party,
    r.votes,
    r.candidate
FROM results r 
JOIN county_highest_votes chv ON r.state = chv.state
    AND r.county = chv.county 
    AND r.party = chv.party 
    AND r.votes = chv.votes
;

