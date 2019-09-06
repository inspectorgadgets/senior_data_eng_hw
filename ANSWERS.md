# Senior Data Eng Homework Answers

To answer the questions I used a SQL client to connect to the Postgres DB running in the docker container. 

---

## 1. What is the number of unique users?

**Solution:** 2903

```
select count(distinct user_id) from users;
```

## 2. Who are the marketing ad providers?

**Solution:** Instagram, Facebook, Snapchat & Spotify

```
select distinct provider from marketing;
```

## 3. Which user property is changed the most frequently?

**Solution:** politics

I interpreted *changed* to mean changed **after** their initial setting of a property. I removed the first selection from the overall count of number of changes. I did this because if all 2,903 users initially set their `notifications` property but never modify it, that does not mean it *changes* most frequently.

```
select property
,count(distinct event_id) as property_changes
from (
	select *
	,row_number() over (partition by user_id, property order by event_ts asc) as property_change_index
	from users
) a
where property_change_index != 1
group by 1
order by 2 desc
;
```

## 4. Which ad was showed the most to users who identify as moderates?

**Solution:** ad_id 4

One user can have multiple phones, and one user can have multiple political views over time. I thought the most accurate answer would be to count ad impressions by users across all their phones who *ever* identified as a moderate, as opposed to only counting ad impressions for users *while* they were identifying as a moderate.

```
select m.ad_id
,count(distinct m.event_id) as ad_impressions
from users u
left join marketing m on m.phone_id = u.phone_id
where u.user_id in (
	
	select distinct user_id
	from users 
	where property = 'politics' 
	and value = 'Moderate'

)
group by 1
order by 2 desc
;
```

## 5. What are the top 5 ads? Explain how you arrived at that conclusion.

**Solution:** In descending order of effectiveness: 4, 2, 0, 1, 3

I considered an ad *effective* by ranking them in descending order according to the number of users who saw the ads prior to their first entries in the `users` table. I assumed that a user would only appear in the `users` table if they had created a Hinge account. Viewing an ad and eventually signing up could be a sign that the ad was effective.

|ad_id | users_who_signed_up |
|---|---
|4 | 198 |
|2 | 187 |
|0 | 184 |
|1 | 176 |
|3 | 176 |

```
with first_user_event as (

	select user_id
	,min(event_ts) as first_user_event_ts
	from users 
	group by 1
	
)

select m.ad_id
,count(distinct u.user_id) as users_who_signed_up
from users u
left join marketing m on m.phone_id = u.phone_id
left join first_user_event fue on fue.user_id = u.user_id
where m.event_ts < fue.first_user_event_ts
group by 1
order by 2 desc
;
```