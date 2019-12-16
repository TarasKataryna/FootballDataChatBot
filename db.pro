get_user_competitions(UserId, CompetitionId, CompetitionName) :- 
		competition(CompetitionId, CompetitionName), 
		user_competition(UserId, CompetitionId).
% section.facts

competition(1, 'Premier League').
competition(2, 'Asdads').
user_competition(22, 1).
user_competition(23, 2).
user_competition(23, 1).