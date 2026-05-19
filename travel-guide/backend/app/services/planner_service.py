def schedule_itinerary(places, total_minutes):
    plan = []
    current_time = 0
    
    for place in places:
        duration_val = 60
        if place.duration and 'h' in place.duration:
            duration_val = int(place.duration.split('h')[0].strip()) * 60
        elif place.duration and 'min' in place.duration:
            duration_val = int(place.duration.split('min')[0].strip())
            
        if current_time + duration_val <= total_minutes:
            plan.append(place)
            current_time += duration_val
            
    return plan