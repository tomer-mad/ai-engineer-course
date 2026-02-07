# Titanic Historical Data - Fare & Passenger Statistics

## Executive Summary

**Total Passengers**: 1,309  
**Total Revenue**: $43,550.49  
**Overall Survival Rate**: 38.2%

---

## Class Comparison Table

| Metric | 1st Class | 2nd Class | 3rd Class |
|--------|-----------|-----------|-----------|
| **Passengers** | 323 (24.7%) | 277 (21.2%) | 709 (54.2%) |
| **Average Fare** | **$89.45** | **$21.65** | **$13.38** |
| **Median Fare** | $61.38 | $15.05 | $8.05 |
| **Min Fare** | $5.00 | $9.69 | $3.17 |
| **Max Fare** | $512.33 | $73.50 | $69.55 |
| **Total Revenue** | $28,265.40 | $5,866.64 | $9,418.45 |
| **Survival Rate** | **61.9%** | **43.0%** | **25.5%** |
| **Male %** | 55.4% | 61.7% | 69.5% |
| **Female %** | 44.6% | 38.3% | 30.5% |

---

## Key Insights

### 💰 Fare Analysis

#### 1st Class (Luxury)
- **Average ticket**: $89.45 (paid) / $87.51 (including free)
- **Typical range**: $31.68 - $108.90 (25th-75th percentile)
- **Price distribution**:
  - 67% paid $25-$100
  - 27% paid $100+
  - Most expensive ticket: $512.33
- **Average passenger paid 6.7x more than 3rd class**

#### 2nd Class (Middle)
- **Average ticket**: $21.65
- **Typical range**: $13.00 - $26.00 (25th-75th percentile)
- **Price distribution**:
  - 62% paid $10-$25
  - 33% paid $25-$50
  - Most paid moderate fares
- **Average passenger paid 1.6x more than 3rd class**

#### 3rd Class (Steerage)
- **Average ticket**: $13.38
- **Typical range**: $7.75 - $15.25 (25th-75th percentile)
- **Price distribution**:
  - 67% paid under $10
  - 23% paid $10-$25
  - Cheapest ticket: $3.17
- **Most affordable option for immigrants**

---

## Revenue Distribution

| Class | Revenue | % of Total | Revenue per Passenger |
|-------|---------|------------|----------------------|
| 1st | $28,265.40 | **64.9%** | $87.51 |
| 2nd | $5,866.64 | 13.5% | $21.18 |
| 3rd | $9,418.45 | 21.6% | $13.30 |
| **Total** | **$43,550.49** | 100% | $33.27 |

**Key Finding**: Despite being only 24.7% of passengers, 1st class generated nearly 65% of all revenue!

---

## Survival Statistics by Class

### Overall Survival Rates
- **1st Class**: 61.9% survived (200/323)
- **2nd Class**: 43.0% survived (119/277)
- **3rd Class**: 25.5% survived (181/709)

### Gender Survival Rates

#### 1st Class
- **Women**: 96.5% survived (139/144)
- **Men**: 34.1% survived (61/179)
- **Gender gap**: 62.4 percentage points

#### 2nd Class
- **Women**: 88.7% survived (94/106)
- **Men**: 14.6% survived (25/171)
- **Gender gap**: 74.1 percentage points

#### 3rd Class
- **Women**: 49.1% survived (106/216)
- **Men**: 15.2% survived (75/493)
- **Gender gap**: 33.9 percentage points

**Key Finding**: "Women and children first" policy clearly evident across all classes!

---

## Passenger Demographics by Class

| Class | Total | Male | Female | Male % | Female % |
|-------|-------|------|--------|--------|----------|
| 1st | 323 | 179 | 144 | 55.4% | 44.6% |
| 2nd | 277 | 171 | 106 | 61.7% | 38.3% |
| 3rd | 709 | 493 | 216 | 69.5% | 30.5% |
| **Total** | **1,309** | **843** | **466** | **64.4%** | **35.6%** |

**Observations**:
- More men than women in all classes
- 3rd class had highest proportion of men (69.5%)
- 1st class had most balanced gender ratio

---

## Fare Distribution Details

### 1st Class Fare Breakdown
| Fare Range | Passengers | Percentage |
|------------|------------|------------|
| < $10 | 1 | 0.3% |
| $10-$25 | 0 | 0.0% |
| $25-$50 | 104 | 32.9% |
| $50-$100 | 127 | 40.2% |
| $100+ | 84 | 26.6% |

**Most common range**: $50-$100 (40.2%)

### 2nd Class Fare Breakdown
| Fare Range | Passengers | Percentage |
|------------|------------|------------|
| < $10 | 1 | 0.4% |
| $10-$25 | 168 | 62.0% |
| $25-$50 | 90 | 33.2% |
| $50-$100 | 12 | 4.4% |
| $100+ | 0 | 0.0% |

**Most common range**: $10-$25 (62.0%)

### 3rd Class Fare Breakdown
| Fare Range | Passengers | Percentage |
|------------|------------|------------|
| < $10 | 472 | 67.0% |
| $10-$25 | 162 | 23.0% |
| $25-$50 | 51 | 7.2% |
| $50-$100 | 19 | 2.7% |
| $100+ | 0 | 0.0% |

**Most common range**: < $10 (67.0%)

---

## Statistical Percentiles (Paid Fares Only)

### 1st Class
- **25th percentile**: $31.68
- **50th percentile (Median)**: $61.38
- **75th percentile**: $108.90
- **90th percentile**: $211.50

### 2nd Class
- **25th percentile**: $13.00
- **50th percentile (Median)**: $15.05
- **75th percentile**: $26.00
- **90th percentile**: $36.75

### 3rd Class
- **25th percentile**: $7.75
- **50th percentile (Median)**: $8.05
- **75th percentile**: $15.25
- **90th percentile**: $24.15

---

## Special Cases

### Free Tickets ($0 Fare)
- **Total**: 17 passengers (1.3% of all passengers)
- **1st Class**: 7 passengers
- **2nd Class**: 6 passengers
- **3rd Class**: 4 passengers
- **Likely**: Crew members, employees, or special cases

### Missing Fare Data
- **Total**: 1 passenger (0.08%)
- Very complete dataset!

---

## Economic Analysis

### Revenue Concentration
```
1st Class: █████████████████████████████████████████████████████████████ 64.9%
2nd Class: █████████████ 13.5%
3rd Class: █████████████████████ 21.6%
```

### Passenger Distribution
```
1st Class: ████████████████████████ 24.7%
2nd Class: █████████████████████ 21.2%
3rd Class: ██████████████████████████████████████████████████████ 54.2%
```

**Key Insight**: 1st class was 24.7% of passengers but generated 64.9% of revenue - a premium segment!

---

## What This Means for the Ticket System

### Realistic Fare Recommendations

**Budget Traveler** (3rd Class):
- Aim for: $7-$15
- Most common: $8.05 (median)
- Survival odds: ~25%

**Middle Class** (2nd Class):
- Aim for: $13-$26
- Most common: $15.05 (median)
- Survival odds: ~43%

**Wealthy Passenger** (1st Class):
- Aim for: $31-$109
- Most common: $61.38 (median)
- Survival odds: ~62%

**Very Wealthy** (Premium 1st Class):
- Above $109 (top 25%)
- Maximum: $512.33
- Best survival odds + female = ~96.5%

---

## Historical Context

### Why Such Different Survival Rates?

1. **Location on Ship**:
   - 1st class cabins on upper decks (easier lifeboat access)
   - 3rd class cabins in lower decks (harder to reach lifeboats)

2. **Social Protocol**:
   - "Women and children first" strictly enforced
   - 1st class women had 96.5% survival (priority boarding)
   - 3rd class men had only 15.2% survival

3. **Economic Reality**:
   - 1st class paid 6.7x more but had 2.4x better survival odds
   - Money could literally buy better survival chances

---

## Data Quality Notes

- **Very complete dataset**: Only 1 missing fare value (99.9% complete)
- **17 free tickets**: Likely crew, staff, or special circumstances
- **All classes represented**: Good distribution across economic strata
- **Age data**: 263 missing ages (20% missing), but 80% complete

---

## Conclusion

The Titanic's fare structure clearly shows the economic stratification of early 20th century society:

- **1st Class**: Luxury passengers paying premium prices ($89 average)
- **2nd Class**: Middle-class travelers ($22 average)
- **3rd Class**: Immigrants and working class ($13 average)

Survival rates correlate strongly with class, with 1st class passengers having more than double the survival rate of 3rd class passengers (61.9% vs 25.5%).

The "women and children first" protocol was remarkably effective in 1st class (96.5% female survival) but less so in 3rd class (49.1% female survival), suggesting that class distinctions affected rescue priorities.
