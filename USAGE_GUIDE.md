# 📚 USAGE GUIDE & SCENARIOS

## Getting Started with Examples

This guide walks through real-world scenarios for using the dashboard to maximize earnings.

---

## 🎯 Scenario 1: New Driver (First Time)

**Goal:** Understand when and where to drive

### Step 1: Open Dashboard
```bash
streamlit run app.py
```

### Step 2: Explore Default View
- Sidebar shows: "Cary" location, 8:00-22:00 hours, 1.0x surge, 8-hour shift
- Profit Summary shows: ~₹19,000 for the day
- Earnings per hour: ~₹2,376

### Step 3: Recommendations
Dashboard suggests:
- **🔴 HIGH**: Drive during peak hour (2:00 PM) - Earn extra ₹850/trip
- **🟡 MEDIUM**: Rank #1 location - You're in a top earner area
- **🟢 LOW**: 8-hour shifts optimal

### Step 4: View Best Hours
Chart shows: Top hours are 2-3 PM, 4-5 PM (afternoon peak)

### Step 5: Check Heatmap
- Hottest (Green): Afternoon hours, Downtown areas
- Coolest (Red): Early morning, remote areas

---

## 🎯 Scenario 2: Shift Optimization

**Goal:** Find the most profitable shift time

### Configuration
Change sidebar:
- Location: Keep "Cary"
- Start hour: 8 AM
- End hour: 4 PM (8-hour morning shift)
- Surge: Toggle OFF (1.0x)

### Observe
- Morning shift: ₹8,500 total, ₹1,062/hour
- Evening shift: ₹14,200 total, ₹1,775/hour
- Night shift: ₹3,200 total, ₹400/hour

### Decision
👉 **Best: 5 PM - 1 AM evening shift** (highest hourly rate)

### Use Shift Comparison
Click tab "⚖️ Shift Comparison" to see all options side-by-side:

| Shift | Total Earnings | Per Hour | Trips |
|-------|-----------------|----------|-------|
| Morning | ₹8,500 | ₹1,062 | 12 |
| Afternoon | ₹12,300 | ₹1,538 | 16 |
| Evening | ₹14,200 | ₹1,775 | 18 |
| Night | ₹3,200 | ₹400 | 4 |

---

## 🎯 Scenario 3: Weekend vs Weekday Strategy

**Goal:** Should I drive weekends?

### Check Daily Breakdown
Scroll to "Earnings Trends" → Look at "Daily Trend"

**Data shows:**
- Monday-Friday: ₹12,000-15,000 per day
- Saturday: ₹18,000 per day 📈
- Sunday: ₹16,500 per day

### Recommendation
👉 **Weekends are MORE profitable** by ~20-30%

### Action
- Work Sat-Sun for extra earnings
- Take one weekday off as rest

---

## 🎯 Scenario 4: Location Hopping Strategy

**Goal:** Find the most profitable location to drive

### Use "Best Locations" Section
- Shows top 5 locations by earnings
- Lists: Downtown, Midtown, Uptown, Financial District, etc.

### Example Results
```
1. Downtown: ₹22,000/week (Top earner)
2. Midtown: ₹19,500/week
3. Financial District: ₹18,200/week
4. Uptown: ₹15,600/week
5. Park Area: ₹12,400/week
```

### Decision Flow
1. Check if your current location is in top 5 ✓
2. If not, consider moving to a top location
3. Try it for a week
4. Return to dashboard and check results

### Use Heatmap
- Hover over different locations
- See which hours they're busy
- Plan your timing accordingly

---

## 🎯 Scenario 5: Surge Pricing Exploitation

**Goal:** Maximize earnings using surge multipliers

### Baseline (No Surge)
- Settings: 6 PM - 2 AM, Downtown
- Earnings: ₹8,000
- Per hour: ₹1,000

### What-If: 1.5x Surge
- Earnings: ₹12,000 (+50%)
- Per hour: ₹1,500

### What-If: 2.0x Surge
- Earnings: ₹16,000 (+100%)
- Per hour: ₹2,000

### Strategy
1. **Enable surge pricing toggle** in sidebar
2. Adjust multiplier with slider
3. Watch earnings update in real-time
4. See surge impact instantly

### Recommendation
👉 **Target surge hours!** During high-demand periods (7-9 PM, 11 PM - 1 AM):
- Surge multiplier likely 1.5x-2.0x
- Earnings potential: ₹1,500-2,000 per hour
- Could earn ₹6,000-8,000 in one 4-hour surge period

---

## 🎯 Scenario 6: Idle Time Impact

**Goal:** Understand how waiting time affects earnings

### View Idle Time Analysis
Scroll to bottom → "⏸️ Idle Time Analysis"

**Shows:**
- Downtown: 5 min avg idle (GOOD) 🟢
- Suburbs: 20 min avg idle (MODERATE) 🟡
- Remote: 45 min avg idle (BAD) 🔴

### Calculation Example
**Downtown Trip (2 hours total):**
- Active driving: 1h 40m
- Idle/waiting: 20m
- Earnings: ₹1,500
- **Efficiency: 83%** ✓

**Remote Trip (2 hours total):**
- Active driving: 1h 15m
- Idle/waiting: 45m
- Earnings: ₹1,300
- **Efficiency: 62%** ✗

### Decision
👉 **Downtown is more efficient** - Less waiting, more earning

---

## 🎯 Scenario 7: What-If Analysis (Advanced)

**Goal:** Explore different combinations

### Use What-If Section
1. Adjust surge multiplier: 1.0x → 2.0x
2. Adjust shift duration: 4h → 12h
3. Watch both charts update simultaneously

**Surge Multiplier Impact Chart:**
- Horizontal axis: Surge (1.0x to 2.0x)
- Vertical axis: Total earnings
- See linear increase in earnings

**Shift Duration Impact Chart:**
- Horizontal axis: Hours (2h to 12h)
- Vertical axis: Total earnings
- Shows diminishing returns after 10 hours (fatigue kicks in)

### Optimal Combination
From the charts, determine:
- **Best surge timing**: When multiplier reaches 2.0x (usually 11 PM - 1 AM)
- **Best shift length**: 8 hours (sweet spot between earnings and fatigue)
- **Recommendation**: "Work 6 PM - 2 AM during Saturday night surge" 💰

---

## 🎯 Scenario 8: Daily Profit Plan

**Goal:** Create an optimized daily schedule

### Morning (6 AM - 12 PM)
1. Check dashboard for morning demand
2. Set hours: 6 - 12
3. Note: ₹6,500 earnings expected
4. Plan: Light traffic, good for steady work

### Afternoon (12 PM - 6 PM)
1. Set hours: 12 - 18
2. Note: ₹9,200 earnings expected
3. Peak demand period
4. Strategy: Maximize trips during 2-5 PM surge

### Evening (6 PM - 12 AM)
1. Set hours: 18 - 24
2. Note: ₹13,500 earnings expected
3. Highest surge periods
4. Strategy: Use surge multiplier 1.5-2.0x

### Total Potential Daily Earnings
- Morning: ₹6,500
- Afternoon: ₹9,200
- Evening: ₹13,500
- **Total: ₹29,200** (12-hour day)
- **Per hour: ₹2,433** (very good!)

---

## 🎯 Scenario 9: Location Comparison

**Goal:** Decide between two locations

### Setup Comparison
**Location A: Downtown**
1. Select "Downtown" from sidebar
2. Set standard hours (9-5)
3. Note metrics: ₹12,000, ₹1,500/hr, 16 trips

**Location B: Suburbs**
1. Select "Suburbs" from sidebar
2. Same hours (9-5)
3. Note metrics: ₹8,000, ₹1,000/hr, 10 trips

### Analysis
| Metric | Downtown | Suburbs |
|--------|----------|---------|
| Total Earnings | ₹12,000 | ₹8,000 |
| Per Hour | ₹1,500 | ₹1,000 |
| Trips | 16 | 10 |
| Idle Time | 15 min | 25 min |
| Recommendation | ✓ BETTER | • Less optimal |

### Decision
👉 **Choose Downtown** - 50% higher earnings!

---

## 🎯 Scenario 10: Monthly Planning

**Goal:** Project monthly earnings

### Use Daily Metrics
Typical daily earnings from dashboard:
- **Weekday (Mon-Fri):** ₹12,000
- **Weekend (Sat-Sun):** ₹16,000

### Calculate Monthly
```
Weekdays: 20 days × ₹12,000 = ₹240,000
Weekends: 8 days × ₹16,000 = ₹128,000
Total Monthly: ₹368,000
```

### Yearly Projection
```
Monthly average: ₹368,000
Yearly estimate: ₹4,416,000
```

### Optimization Opportunities
- Switch to evening shifts (+20%): ₹5,299,200
- Target surge hours (+30%): ₹5,740,800
- Use both strategies (+50%): ₹6,624,000

---

## 💡 Pro Tips

### Tip 1: Time Your Shifts
- **Best:** 5 PM - 1 AM (evening/night)
- **Good:** 12 PM - 6 PM (afternoon)
- **Okay:** 6 AM - 12 PM (morning)
- **Avoid:** 12 AM - 6 AM (midnight to early morning)

### Tip 2: Follow the Heatmap
- **Dark Green areas:** High demand + high earnings
- **Yellow areas:** Moderate (average demand)
- **Red areas:** Low demand (avoid if possible)

### Tip 3: Idle Time Matters
- **Low idle (<10 min):** Downtown areas
- **Medium idle (15-20 min):** Suburban areas
- **High idle (>30 min):** Remote areas
- **Choose:** Minimize idle time for better hourly rate

### Tip 4: Surge Hour Strategy
- Watch for surge multipliers (1.5x+)
- Check recommendations for peak hours
- Plan your busiest hours during surge
- Example: 11 PM - 1 AM usually sees 1.5-2.0x surge

### Tip 5: Location Switching
- Don't stay in same location all day
- Use heatmap to find where demand shifts
- For example: Morning in Downtown, Evening in Uptown
- Adapt based on hourly patterns

### Tip 6: Week Planning
- Check daily breakdown
- Weekends are 20-30% more profitable
- Plan 2-3 extra hours on Sat-Sun
- Take one weekday off as compensation

### Tip 7: Use What-If Analysis
- Experiment before committing
- See surge impact instantly
- Understand shift duration trade-offs
- Make data-driven decisions

### Tip 8: Monitor Idle Time
- Long idle periods reduce effective hourly rate
- Example: 45-min idle = 23% efficiency loss
- Prioritize locations with <15 min idle
- Worth 20+ minutes of driving to reduce idle

---

## 🚨 Common Mistakes to Avoid

### ❌ Mistake 1: Ignoring Idle Time
- Drives to remote area for 1-2 trips
- Spends 30+ minutes waiting between rides
- Effective hourly rate drops by 30%
- 👉 **Fix:** Use heatmap, stay in high-demand areas

### ❌ Mistake 2: Wrong Time Selection
- Drives steady 9 AM - 5 PM
- Misses evening surge (1.5-2.0x)
- Loses ₹3,000-5,000 potential earnings
- 👉 **Fix:** Check recommendations, shift to 5 PM - 1 AM

### ❌ Mistake 3: Not Using Surge
- Disables surge multiplier toggle
- Doesn't realize impact of surge
- Loses 50-100% potential earnings during surge hours
- 👉 **Fix:** Enable surge, set to max during peak hours

### ❌ Mistake 4: Wrong Location Choice
- Picks low-demand area
- Gets ₹400/hr instead of ₹1,500/hr
- Wastes time in inefficient locations
- 👉 **Fix:** Use "Best Locations" ranking, prioritize top 5

### ❌ Mistake 5: Over-Shifting
- Works 14+ hour days
- Quality drops, concentration wanes
- Safety risks increase
- Effective hourly rate plateaus
- 👉 **Fix:** Dashboard recommends 8 hours max, stick to it

---

## 📊 Dashboard Quick Reference

### Sidebar Controls
| Control | Range | Impact |
|---------|-------|--------|
| Location | All locations | Changes earnings by 50-300% |
| Start hour | 0-23 | Picks shift start time |
| End hour | 0-23 | Picks shift end time |
| Surge multiplier | 1.0-2.0x | Increases earnings proportionally |
| Shift hours | 1-24 | Affects total earnings |

### Key Metrics (Metric Cards)
| Metric | What It Means | Good Range |
|--------|---------------|------------|
| Total Earnings | Expected daily earnings | ₹10,000-20,000 |
| Earnings/Hour | Average hourly rate | ₹1,200-1,800 |
| Estimated Trips | Number of trips projected | 12-20 per 8h |
| Idle Time | Average waiting time | <20 minutes |

### Charts (What to Look For)
| Chart | Best Pattern | Bad Pattern |
|-------|--------------|------------|
| Demand Heatmap | Green corners, many hot spots | Red areas, sparse green |
| Trends | Peaks at specific hours | Flat/no clear pattern |
| What-If | Linear increase with surge | No change (no impact) |
| Shift Comp | One shift clearly better | All roughly equal |

---

## 🎓 Learning Path

### Beginner (Day 1)
- [ ] Open dashboard
- [ ] Explore default view
- [ ] Read profit summary cards
- [ ] View recommendations
- [ ] Look at best hours/locations

### Intermediate (Week 1)
- [ ] Try different locations
- [ ] Adjust working hours
- [ ] Toggle surge pricing
- [ ] Run What-If scenarios
- [ ] Compare shifts
- [ ] Check idle time analysis

### Advanced (Week 2+)
- [ ] Optimize daily schedule
- [ ] Plan weekly rotation
- [ ] Target surge hours
- [ ] Track actual vs projected
- [ ] Refine strategies
- [ ] Maximize earnings

---

## 🎉 Success Metrics

### Week 1 Goal
- [ ] Understand dashboard features
- [ ] Identify best location for you
- [ ] Know top 3 earning hours
- [ ] See earning potential increase by 20%

### Month 1 Goal
- [ ] Optimize shift timing
- [ ] Increase hourly rate by 30%
- [ ] Plan efficient weekly schedule
- [ ] Use surge multiplier strategically

### Quarter 1 Goal
- [ ] Maximize earnings 50% above starting point
- [ ] Become expert at dashboard
- [ ] Share tips with other drivers
- [ ] Reach ₹1,500+/hour consistently

---

**Happy optimizing! Your earnings are about to improve significantly! 💰📈**
