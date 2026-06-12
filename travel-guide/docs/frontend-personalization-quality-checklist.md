# Frontend Personalization Quality Checklist

Use this checklist when validating itinerary personalization from the browser.

## Test Profiles

### Culture-focused relaxed trip
- Select categories: `culture`, `art`, `landmark`
- Intensity: `Relaxed`
- Transport: `Walking`
- Days: `2`
- Expected result:
  - Itinerary prefers selected categories.
  - No day exceeds the relaxed daily limit.
  - Breaks can be added only while the day remains feasible.
  - Overflow appears instead of forcing an impossible schedule.

### Outdoor and family moderate trip
- Select categories: `outdoor`, `family`, `food`
- Intensity: `Moderate`
- Transport: `Transit`
- Days: `1`
- Expected result:
  - Planned attractions match the selected categories.
  - Travel slots and break slots remain in chronological order.
  - Late or unrealistic schedules show visible warnings.

### High-intensity mixed trip
- Select all categories.
- Intensity: `Intense`
- Transport: `Cycling`
- Days: `1`
- Expected result:
  - The app creates a fuller day than relaxed or moderate modes.
  - Reordering attractions does not create invalid schedules.
  - Long travel segments are flagged.

## Regression Checks

- Generate itinerary with no backend running for `/places`; the frontend shows the API error state.
- Select and deselect categories; attraction filtering still follows the selected categories.
- Select attractions, generate itinerary, reorder attractions, remove attractions, add breaks, remove breaks, and change break duration.
- Try increasing a break until the day would exceed the intensity limit; the app blocks the change and shows a message.
- Try profiles with narrow categories and confirm the app does not generate irrelevant attractions when matching attractions exist.
- Confirm no empty itinerary is produced when selected attractions are available.

## Related Issues

- #83 Test personalization quality
- #95 Validate schedule after breaks
- #106 Validate realistic schedules
- #68 Validate itinerary feasibility
- #78 Prevent scheduling conflicts
