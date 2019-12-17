get_user_competitions(UserId, CompetitionId) :- 
		competition(CompetitionId), 
		user_competition(UserId, CompetitionId).
% section.facts

competition(1).
user_competition(22, 1).
competition(2).
user_competition(23, 2).
user_competition(23, 1).
user_competition(22, 2).