from typing import List
from uuid import UUID
from datetime import datetime, timezone
from sqlmodel import select

from core.db import SessionDep
from api.models import (
    Brand,
    Campaign,
    StrategicGoal,
    Audience,
    Demographic,
    Trigger,
    User
)


async def run_seed_for_user(user_id: UUID, session: SessionDep) -> Brand:
    # Check if brand already exists for user
    stmt = select(Brand).where(
        Brand.user_id == user_id,
        Brand.name == "Only Murders In The Building"
    )
    existing_brand = session.exec(stmt).first()
    if existing_brand:
        return existing_brand

    # Create brand
    brand = Brand(
        name="Only Murders In The Building",
        website_url="https://www.hulu.com/series/only-murders-in-the-building",
        user_id=user_id,
        about="""Only Murders in the Building, a Hulu-exclusive series, enchants and engages audiences by weaving compelling narratives into extraordinary experiences. The series captivates viewers with its intricate storytelling and unique blend of mystery and humor, ensuring a memorable viewing journey. It has quickly become a fan favorite, drawing viewers into its intriguing world filled with suspense and wit, setting a new standard for television entertainment.The show's fundamental principles are anchored in prioritizing the audience, embracing an innovative approach, and cultivating a culture built on unwavering respect and trust. It underscores the necessity of revolutionizing television and is committed to nurturing an environment of collaboration, inclusivity, and creativity. By pushing the boundaries of traditional storytelling, Only Murders in the Building fosters a community of diverse voices and perspectives, making it not only a must-watch but also a beacon of modern television's potential.""",
        key_characteristics="""- Innovative storytelling: Hulu's 'Only Murders in The Building' combines compelling narratives with unique experiences, setting a new standard for television.
        - Audience-centric approach: The show prioritizes its audience, ensuring captivating and engaging content that resonates with viewers.
        - Culture of respect and inclusivity: It fosters an environment that values collaboration, inclusivity, and creativity, reflecting in the show's production and execution.
        - Commitment to revolutionizing television: The show is committed to disrupting traditional television norms, offering a refreshing and innovative viewing experience.""",
        category="Streaming Entertainment",
        positioning="Light and intriguing entertainment for fans of mystery and humor.",
        traditional_target_audience="""- Demographic: Adults aged 18-45 with an interest in comedy, mystery, and true crime genres.
        - Demographic: Individuals who have a high consumption of digital media and streaming platforms, particularly Hulu.
        - Psychographic: Viewers who value innovative and original storytelling that combines humor, suspense, and social commentary.
        - Psychographic: Engaged audience members who enjoy interactive experiences and tend to participate in online communities or discussion forums related to television series.""",
        key_competitors="""1. Netflix - "Stranger Things": A globally recognized streaming platform, its original series "Stranger Things" is a unique blend of science fiction, drama, and horror, which sets it apart. Netflix's strong point lies in its vast library of content and its ability to consistently produce high-quality, binge-worthy series like "Stranger Things".

2. Amazon Prime Video - "The Marvelous Mrs. Maisel": Prime Video differentiates itself with award-winning original content like "The Marvelous Mrs. Maisel", a comedy-drama set in the late 1950s. Amazon Prime Video's strength lies in its combination of a diverse content library, including movies, TV series, and documentaries, along with added benefits for Amazon Prime members.

3. HBO Max - "Succession": Known for its premium, critically acclaimed original series like "Succession", HBO Max stands out with its mature, thought-provoking content. The platform differentiates itself with its commitment to high production values and storytelling depth, often focusing on complex, character-driven narratives.""",
        first_access=False,
        brand_summary_active=True,
        strategic_goals_active=True,
        audience_active=True,
        brand_universe_active=True,
        ad_legacy_active=True
    )

    session.add(brand)
    session.commit()
    session.refresh(brand)

    # Create campaign
    campaign = Campaign(
        campaign="Initial Campaign",
        brand_id=brand.id,
        is_active=True,
        is_completed=False
    )
    session.add(campaign)
    session.commit()
    session.refresh(campaign)

    # Create strategic goals
    strategic_goals = [
        StrategicGoal(
            strategic_goal="Increase Hulu's subscriptions",
            campaign_id=campaign.id,
            is_active=True,
            strategic_goal_color="#3FE2E8"

        ),
        StrategicGoal(
            strategic_goal="Retain Hulu's paid customers",
            campaign_id=campaign.id,
            is_active=True,
            strategic_goal_color="#FF36C3"
        ),
        StrategicGoal(
            strategic_goal="Minimize Hulu's churn rate",
            campaign_id=campaign.id,
            is_active=True,
            strategic_goal_color="#FFD036"
        )
    ]

    for goal in strategic_goals:
        session.add(goal)
    session.commit()
    for goal in strategic_goals:
        session.refresh(goal)

    # Create audiences with demographics and triggers
    audiences_data = [
        {
            "audience": {
                "name": "Hispanic Families",
                "description": "Proud, tradition-focused families seeking affordable, culturally aligned products.",
                "psycho_graphic": "Family-oriented, value cultural traditions, and prioritize strong community ties.",
                "attitudinal": "I am proud of my heritage and value staying connected to my family and community.",
                "self_concept": "I see myself as a provider who strengthens family bonds and ensures we honor our traditions.",
                "lifestyle": "Family-oriented, often larger households with strong cultural traditions and values.",
                "media_habits": "Regular viewers of Spanish-language networks, telenovelas, soccer games, and family shows.",
                "general_keywords": "Family traditions, Cultural pride, Bilingual communication",
                "brand_keywords": "Family mystery night, Crime-solving fun, Bilingual storytelling",
                "key_tags": "Proud Heritage, Family Traditions, Bilingual Entertainment",
                "brand_id": brand.id,
                "image_url": "SEED1A1.jpg",
            },
            "demographic": {
                "gender": "Both",
                "age_bracket": "25-54",
                "hhi": "75k-150k",
                "ethnicity": "Primarily Hispanic or Latino",
                "education": "High school diploma to some college",
                "location": "Urban centers like Los Angeles, Miami, Houston, and New York City"
            },
            "triggers": [
                {
                    "name": "Familia Fiesta Mystery Night",
                    "description": "Gather the family for a bilingual mystery filled with humor and heartfelt moments.",
                    "territory": "Mystery",
                    "trigger_img": "SEED1A1T1.jpg",
                    "image_prompt": "test"

                },
                {
                    "name": "Movie Night Under the Stars",
                    "description": "Hosting a movie night with loved ones can evoke nostalgia and create lasting memories, especially in Latin households. This trigger encourages families to choose Hulu for their viewing pleasure, emphasizing the platform's vast library of films and series that cater to cultural interests. The excitement of sharing stories and laughter during these nights solidifies the need for an ongoing subscription.",
                    "territory": "Star Power",
                    "trigger_img": "SEED1A1T2.jpg",
                    "image_prompt": "test"

                },
                {
                    "name": "Milestone Celebrations",
                    "description": "Key personal milestones such as birthdays, anniversaries, or graduations are cherished in Hispanic families. These events often serve as opportunities for gathering and reflecting on shared milestones, where Hulu’s relatable content can enhance the celebratory atmosphere. By showcasing exclusive content catering to these occasions, families are motivated to retain their subscriptions and explore new offerings for future events.",
                    "territory": "Milestone Celebrations",
                    "trigger_img": "SEED1A1T3.jpg",
                    "image_prompt": "test"
                }
            ]
        },
        {
            "audience": {
                "name": "Value-Seeking Single Mom",
                "description": "Budget-savvy caregiver prioritizing practicality and family bonding.",
                "psycho_graphic": "Focused on stretching their dollar without compromising on quality.",
                "attitudinal": "I want to make smart financial decisions that benefit my family.",
                "self_concept": "I see myself as resourceful and committed to providing a comfortable life for my family.",
                "lifestyle": "Balancing expenses and focused on value purchases.",
                "media_habits": "Viewers of prime-time family TV, syndicated sitcoms, and sports.",
                "general_keywords": "Family savings, Value for money, Smart shopping",
                "brand_keywords": "Affordable entertainment, Family mystery marathon, Cozy crime shows",
                "key_tags": "Budget Friendly, Family First, Practical Solutions",
                "brand_id": brand.id,
                "image_url": "SEED1A2.jpg",
            },
            "demographic": {
                "gender": "Female",
                "age_bracket": "25-44",
                "hhi": "50k-75k",
                "ethnicity": "White and African American, skewed African American",
                "education": "High school diploma to some college",
                "location": "Suburban, small cities or rural areas"
            },
            "triggers": [
                {
                    "name": "Mystery Night Without the Splurge",
                    "description": "Affordable, wholesome entertainment for the whole family. Dive into a quirky mystery series that’s perfect for cozy nights at home—no expensive tickets or subscriptions required.",
                    "territory": "Mystery",
                    "trigger_img": "SEED1A2T1.jpg",
                    "image_prompt": "test"
                },
                {
                    "name": "Seasonal Series Binge-Watch",
                    "description": "The onset of a new season prompts viewers to seek fresh and exciting content. As cooler temperatures invite people indoors, they turn to Hulu for series that captivate their interest and provide escape. This is the perfect time for subscribers to dive into compelling stories and notable characters, enhancing their viewing experience and fostering emotional connections with the content.",
                    "territory": "Star Power",
                    "trigger_img": "SEED1A2T2.jpg",
                    "image_prompt": "test"
                },
                {
                    "name": "New Year, New Beginnings",
                    "description": "As the new year approaches, many individuals reflect on personal growth and new resolutions. Subscriptions to Hulu become not just an entertainment choice but a partner in achieving personal aspirations like self-care or family time. With Fresh starts in mind, Hulu offers a diverse selection of uplifting content to inspire and motivate viewers to kick off their year positively and purposefully.",
                    "territory": "New Beginnings",
                    "trigger_img": "SEED1A2T3.jpg",
                    "image_prompt": "test"
                }
            ]
        },
        {
            "audience": {
                "name": "Young, Trendy Millennials",
                "description": "Passionate about crime stories and investigative narratives.",
                "psycho_graphic": "Trend-driven, socially conscious, and tech-savvy.",
                "attitudinal": "I am drawn to innovative and socially responsible brands that align with my values.",
                "self_concept": "I see myself as a trendsetter who is culturally aware.",
                "lifestyle": "Tech-savvy, socially conscious, and driven by trends.",
                "media_habits": "Late-night shows, premium streaming services, and live event programming.",
                "general_keywords": "Digital natives, Tech-savvy lifestyle, Trendsetters",
                "brand_keywords": "True crime obsession, Podcast culture, Modern whodunit",
                "key_tags": "Trendsetters, TechSavvy, BuzzWorthy",
                "brand_id": brand.id,
                "image_url": "SEED1A3.jpg",
            },
            "demographic": {
                "gender": "Both",
                "age_bracket": "25-44",
                "hhi": "75k-150k",
                "ethnicity": "Diverse",
                "education": "College degree or higher",
                "location": "Urban areas such as New York, Chicago, Los Angeles, and Austin"
            },
            "triggers": [
                {
                    "name": "Binge-Worthy Whodunit",
                    "description": "Join the cultural conversation! 'Only Murders in the Building' delivers stylish mysteries, modern twists, and Selena Gomez’s iconic performance—perfect for your next binge-watch session.",
                    "territory": "True Crime Podcast",
                    "trigger_img": "SEED1A3T1.jpg",
                    "image_prompt": "test"
                },
                {
                    "name": "Cozy Evenings",
                    "description": "As the weather turns colder, trendy millennials look for activities that allow them to unwind after a busy week. The desire for comfort and relaxation during the fall and winter months evokes a need for cozy nights in and binge-watching sessions with friends. Hulu can be their go-to source for captivating series and movies that enhance these moments, transforming their evenings into memorable experiences filled with shared laughter and suspense.",
                    "territory": "The Building",
                    "trigger_img": "SEED1A3T2.jpg",
                    "image_prompt": "test"
                },
                {
                    "name": "Milestone Celebrations",
                    "description": "Young millennials often celebrate significant milestones, such as moving into their first apartments or landing their dream jobs. These events inspire them to seek out entertainment options that elevate their celebratory moments. Hulu presents itself as a perfect companion for parties and gatherings, featuring content that resonates with their unique experiences and stories of success, making the platform a staple for social events.",
                    "territory": "Star Power",
                    "trigger_img": "SEED1A3T3.jpg",
                    "image_prompt": "test"
                }
            ]
        },
        {
            "audience": {
                "name": "Active Boomers",
                "description": "Wellness-minded retirees enjoying nostalgia and classic comedy.",
                "psycho_graphic": "Emphasize active living, wellness, and staying engaged in retirement.",
                "attitudinal": "I focus on staying healthy, active, and independent as I age.",
                "self_concept": "I see myself as vibrant, youthful, and ready to enjoy life to its fullest.",
                "lifestyle": "Focused on health, wellness, and active living.",
                "media_habits": "Morning talk shows, daytime TV, news, and golf or baseball sports programming.",
                "general_keywords": "Active retirement, Senior wellness, Healthy aging",
                "brand_keywords": "Steve Martin and Martin Short nostalgia, Light-hearted crime-solving",
                "key_tags": "Nostalgia, Wellness, Lighthearted Mystery",
                "brand_id": brand.id,
                "image_url": "SEED1A4.jpg",
            },
            "demographic": {
                "gender": "Male",
                "age_bracket": "65+",
                "hhi": "150k-250k",
                "ethnicity": "Primarily White",
                "education": "High school diploma to college degree",
                "location": "Suburban"
            },
            "triggers": [
                {
                    "name": "Classic Whodunit, Modern Twist",
                    "description": "Rediscover the joy of TV with Steve Martin and Martin Short’s classic comedic charm. 'Only Murders in the Building' offers a clever, lighthearted mystery with a modern twist—perfect for active minds and nostalgic hearts.",
                    "territory": "Star Power",
                    "trigger_img": "SEED1A4T1.jpg",
                    "image_prompt": "test"
                },
                {
                    "name": "Celebration of Milestones",
                    "description": "Milestones such as anniversaries or birthdays prompt Boomers to seek entertainment for gatherings. They value shared experiences, especially when celebrating with loved ones, and lean toward options that provide engaging content suitable for all ages. This trigger encourages them to retain their Hulu subscriptions as it promises a network of diverse programming, creating memorable moments in their lives while ensuring laughter and joy with family and friends.",
                    "territory": "The Building",
                    "trigger_img": "SEED1A4T2.jpg",
                    "image_prompt": "test"
                },
                {
                    "name": "Seasonal Cozy Comedies",
                    "description": "As seasons change, Boomers desire warm, comforting experiences in their downtime. Facing the chill of winter or the occasional rainy day, they seek light-hearted comedies that evoke laughter and joy, providing an escape from daily stresses. This seasonal shift motivates them to minimize churn by finding solace in Hulu’s engaging content, ensuring that their favorite shows are always just a click away during cozy indoor moments.",
                    "territory": "Mystery",
                    "trigger_img": "SEED1A4T3.jpg",
                    "image_prompt": "test"
                }
            ]
        },
        {
            "audience": {
                "name": "Strategic Sports Fans",
                "description": "Competitive enthusiasts who thrive on teamwork and excitement.",
                "psycho_graphic": "Highly passionate and emotionally invested in team activities.",
                "attitudinal": "I am deeply loyal to my favorite teams and enjoy sharing my passion with others.",
                "self_concept": "I see myself as a spirited, team-oriented fan who values competition.",
                "lifestyle": "Passionate about professional sports and team activities.",
                "media_habits": "Viewers of live sports broadcasts, sports analysis, and team coverage.",
                "general_keywords": "Game day excitement, Fantasy leagues, Team loyalty",
                "brand_keywords": "Team up to solve the case, Mystery fans unite, Competition for clues",
                "key_tags": "Team Spirit, Competition, Mystery Play",
                "brand_id": brand.id,
                "image_url": "SEED1A5.jpg",
            },
            "demographic": {
                "gender": "Predominantly male",
                "age_bracket": "18-45",
                "hhi": "75k-150k",
                "ethnicity": "Diverse",
                "education": "High school diploma to bachelor's degree",
                "location": "Urban and suburban"
            },
            "triggers": [
                {
                    "name": "Solve the Play, Crack the Case",
                    "description": "Love strategy and competition? Team up with Steve Martin, Martin Short, and Selena Gomez as they unravel a thrilling whodunit packed with twists, turns, and plenty of laughs.",
                    "territory": "Mystery",
                    "trigger_img": "SEED1A5T1.jpg",
                    "image_prompt": "test"
                },
                {
                    "name": "Milestone Moments",
                    "description": "Celebrating personal milestones such as graduations, engagements, or promotions prompts a desire for risk-free entertainment that can galvanize shared experiences. By positioning Hulu's library of feel-good films and series around these events, it encourages current customers to retain subscriptions to create memorable moments with loved ones.",
                    "territory": "True Crime Podcast",
                    "trigger_img": "SEED1A5T2.jpg",
                    "image_prompt": "test"
                },
                {
                    "name": "Seasonal Significance",
                    "description": "The arrival of different seasons triggers specific viewing habits; for instance, the cozy, introspective mood of autumn inspires binge-watching of beloved series and movies. By promoting themed collections on Hulu that align with the fall season, current subscribers can rediscover content that resonates with their emotional state, aiding in minimizing churn.",
                    "territory": "Star Power",
                    "trigger_img": "SEED1A5T3.jpg",
                    "image_prompt": "test"
                }
            ]
        },
        {
            "audience": {
                "name": "Binge Lovers",
                "description": "These viewers indulge in their love for TV series, especially gripping mysteries.",
                "psycho_graphic": "Value experiences over possessions, prioritize representation in media.",
                "attitudinal": "Open to innovation, driven by social justice.",
                "self_concept": "View themselves as change-makers and advocates for inclusivity.",
                "lifestyle": "Enjoy exploring new cultures, favor engaging experiences.",
                "media_habits": "High engagement with streaming platforms and social media.",
                "general_keywords": "Exploration, Authenticity, Inclusivity",
                "brand_keywords": "Engaging narratives, Relatable characters, Modern themes",
                "key_tags": "Binge-watchers, Streaming Enthusiasts, Trendsetters",
                "brand_id": brand.id,
                "image_url": "SEED1A6.jpg"

            },
            "demographic": {
                "gender": "Both",
                "age_bracket": "35-54",
                "hhi": ">250k",
                "ethnicity": "Predominantly White",
                "education": "Bachelor's degree or higher",
                "location": "Affluent suburbs and urban centers"
            },
            "triggers": [
                {
                    "name": "The Art of the Whodunit",
                    "description": "Step into the world of high-end New York apartments and exclusive mysteries. 'Only Murders in the Building' combines elite wit, luxury living, and a sophisticated yet quirky storyline—perfect for discerning tastes.",
                    "territory": "Mystery",
                    "trigger_img": "SEED1A6T1.jpg",
                    "image_prompt": "test"
                },
                {
                    "name": "Comfort During Life Changes",
                    "description": "During significant life changes, such as moving to a new city or navigating a career transition, people often seek solace in familiar, engaging content. Hulu serves as an emotional refuge, offering viewers a way to unwind and escape from stress during these transitions. By providing supportive and entertaining series that resonate with their experiences, Hulu becomes an essential part of their journey, encouraging continued subscriptions.",
                    "territory": "The Building",
                    "trigger_img": "SEED1A6T2.jpg",
                    "image_prompt": "test"
                },
                {
                    "name": "Exclusive Event Celebration",
                    "description": "Celebrate personal milestones such as birthdays or promotions with a dedicated streaming night featuring Hulu's latest content. Users often seek unique experiences to enhance their special moments, and Hulu can provide exclusive access to vibrant new releases and series. The emotional connection tied to these life events fosters a sense of celebration and togetherness, driving subscriptions to elevate their entertainment choices.",
                    "territory": "Milestone Celebrations",
                    "trigger_img": "SEED1A6T3.jpg",
                    "image_prompt": "test"
                }
            ]
        }
    ]

    for audience_data in audiences_data:
        # Create audience
        audience = Audience(**audience_data["audience"])
        session.add(audience)
        session.commit()
        session.refresh(audience)

        # Create demographic
        demographic = Demographic(
            audience_id=audience.id, **audience_data["demographic"])
        session.add(demographic)
        session.commit()

        # Create triggers
        for trigger_data in audience_data["triggers"]:
            trigger = Trigger(
                audience_id=audience.id,
                # Assign to first goal for simplicity
                strategic_goal_id=strategic_goals[0].id,
                **trigger_data
            )
            session.add(trigger)
        session.commit()

    return brand
