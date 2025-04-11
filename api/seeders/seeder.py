from api.models import (
    Brand,
    BrandInfo,
    Audience,
    StrategicGoals,
    Trigger,
    Demographics,
)

from django.utils import timezone


def run_seed_for_user(user):
    brand, created = Brand.objects.get_or_create(
        name="Only Murders In The Building",
        user=user,
        defaults={
            "brand_url": "https://www.hulu.com/series/only-murders-in-the-building",
            "created_at": timezone.now(),
            "updated_at": timezone.now(),
        },
    )

    if created:
        brand_info, created = BrandInfo.objects.get_or_create(brand=brand)

        brand_info.about = """Only Murders in the Building, a Hulu-exclusive series, enchants and engages audiences by weaving compelling narratives into extraordinary experiences. The series captivates viewers with its intricate storytelling and unique blend of mystery and humor, ensuring a memorable viewing journey. It has quickly become a fan favorite, drawing viewers into its intriguing world filled with suspense and wit, setting a new standard for television entertainment.The show's fundamental principles are anchored in prioritizing the audience, embracing an innovative approach, and cultivating a culture built on unwavering respect and trust. It underscores the necessity of revolutionizing television and is committed to nurturing an environment of collaboration, inclusivity, and creativity. By pushing the boundaries of traditional storytelling, Only Murders in the Building fosters a community of diverse voices and perspectives, making it not only a must-watch but also a beacon of modern television's potential."""
        brand_info.key_characteristics = """- Innovative storytelling: Hulu's 'Only Murders in The Building' combines compelling narratives with unique experiences, setting a new standard for television.- Audience-centric approach: The show prioritizes its audience, ensuring captivating and engaging content that resonates with viewers.- Culture of respect and inclusivity: It fosters an environment that values collaboration, inclusivity, and creativity, reflecting in the show's production and execution.- Commitment to revolutionizing television: The show is committed to disrupting traditional television norms, offering a refreshing and innovative viewing experience."""
        brand_info.category = """Streaming Entertainment"""
        brand_info.positioning = (
            """Entretenimento leve e intrigante para fãs de mistério e humor."""
        )
        brand_info.target_audience = """- Demographic: Adults aged 18-45 with an interest in comedy, mystery, and true crime genres.- Demographic: Individuals who have a high consumption of digital media and streaming platforms, particularly Hulu.- Psychographic: Viewers who value innovative and original storytelling that combines humor, suspense, and social commentary.- Psychographic: Engaged audience members who enjoy interactive experiences and tend to participate in online communities or discussion forums related to television series."""
        brand_info.key_competitors = """1. Netflix - "Stranger Things": A globally recognized streaming platform, its original series "Stranger Things" is a unique blend of science fiction, drama, and horror, which sets it apart. Netflix's strong point lies in its vast library of content and its ability to consistently produce high-quality, binge-worthy series like "Stranger Things".2. Amazon Prime Video - "The Marvelous Mrs. Maisel": Prime Video differentiates itself with award-winning original content like "The Marvelous Mrs. Maisel", a comedy-drama set in the late 1950s. Amazon Prime Video's strength lies in its combination of a diverse content library, including movies, TV series, and documentaries, along with added benefits for Amazon Prime members.3. HBO Max - "Succession": Known for its premium, critically acclaimed original series like "Succession", HBO Max stands out with its mature, thought-provoking content. The platform differentiates itself with its commitment to high production values and storytelling depth, often focusing on complex, character-driven narratives."""

        strategic_goals = [
            "Increase Hulu's subscriptions",
            "Retain Hulu's paid customers",
            "Minimize Hulu's churn rate",
        ]
        for goal in strategic_goals:
            strategic_goal = StrategicGoals.objects.create(brand_id=brand, goal=goal)

        audiences = [
            {
                "name": "Hispanic Families",
                "description": "Proud, tradition-focused families seeking affordable, culturally aligned products. “Familia Fiesta Mystery Night” merges bilingual humor, telenovela flair, and communal fun.",
                "psycho_graphic": "Family-oriented, value cultural traditions, and prioritize strong community ties. Spend on family, celebrations, and products that support multigenerational households.",
                "attitudinal": "I am proud of my heritage and value staying connected to my family and community. I look for products that reflect my traditions and meet the needs of my household. I want affordable, high-quality options that respect and resonate with my culture.",
                "self_concept": "I see myself as a provider who strengthens family bonds and ensures we honor our traditions.",
                "lifestyle": "Family-oriented, often larger households with strong cultural traditions and values.",
                "media_habits": "Regular viewers of Spanish-language networks (Univision, Telemundo), telenovelas, soccer games, and family shows.",
                "general_keywords": "Family traditions, Multigenerational households, Spanish-language TV, Cultural pride, Bilingual communication, Telenovelas, Soccer (fútbol), Community connection, Affordable essentials, Celebrations and fiestas.",
                "brand_keywords": "Family mystery night, Crime-solving fun, Bilingual storytelling, Community bonds, Multi-generational appeal, Telenovela meets comedy, Light-hearted suspense, Family traditions & shows, Diverse characters, New York culture.",
                "image_prompt": "An abstract illustration of a magnifying glass over a cityscape at night with soft shadows.",
                "brand_id": brand.id,
                "key_tags": "Proud Heritage, Family Traditions, Bilingual Entertainment",
                "audience_img": "SEED1A1.jpg",
            },
            {
                "name": "Value-Seeking Single Mom",
                "description": "Budget-savvy caregiver prioritizing practicality and family bonding. “Mystery Night Without the Splurge” delivers cozy, low-cost entertainment for stress-free togetherness.",
                "psycho_graphic": "Focused on stretching their dollar without compromising on quality. Value practicality, discounts, and reliable brands for everyday family needs.",
                "attitudinal": "I want to make smart financial decisions that benefit my family. I prioritize value and quality, and I’m loyal to brands that help me stay within my budget. I prefer practical and efficient solutions that fit my family’s needs.",
                "self_concept": "I see myself as resourceful and committed to providing a comfortable life for my family.",
                "lifestyle": "Balancing expenses and focused on value purchases.",
                "media_habits": "Viewers of prime-time family TV, syndicated sitcoms, and sports.",
                "general_keywords": "Family savings, Value for money, Smart shopping, Discounts and deals, Family meals, Affordable living, Suburban lifestyle, Practical purchases, Everyday essentials, Stretching budgets.",
                "brand_keywords": "Affordable entertainment, Family mystery marathon, Cozy crime shows, Stream-worthy family fun, Value-packed streaming, Wholesome mystery moments, Light-hearted drama, Shared family TV time, Nostalgic humor, Weekend binge-watching.",
                "image_prompt": "A simple couch in a cozy living room setup, with a large screen glowing in a dimly lit environment.",
                "brand_id": brand.id,
                "key_tags": "Budget Friendly, Family First, Practical Solutions",
                "audience_img": "SEED1A2.jpg",
            },
            {
                "name": "Young, Trendy Millennials",
                "description": "Passionate about crime stories, they delve deeply into investigative narratives and complex character developments. Crime dramas are their favorite genre for thrilling escapism.",
                "psycho_graphic": "Trend-driven, socially conscious, and tech-savvy. Prioritize sustainability, modern aesthetics, and experiential over materialistic consumption.",
                "attitudinal": "I am drawn to innovative and socially responsible brands that align with my values. I want products and experiences that are stylish, sustainable, and tech-forward. I care about convenience and brands that enhance my lifestyle.",
                "self_concept": "I see myself as a trendsetter who is culturally aware and part of a progressive, modern community.",
                "lifestyle": "Tech-savvy, socially conscious, and driven by trends.",
                "media_habits": "Late-night shows, premium streaming services, and live event programming.",
                "general_keywords": "Digital natives, Tech-savvy lifestyle, Trendsetters, Social media influencers, Sustainability and eco-conscious, Experiential living, Streaming platforms, Urban culture, Minimalist living, Modern design.",
                "brand_keywords": "True crime obsession, Podcast culture, Modern whodunit, Urban storytelling, Hip & nostalgic humor, Selena Gomez fans, Streaming must-watch, Stylish mystery series, Relatable quirks, Trendy binge culture.",
                "image_prompt": "Silhouette of a detective with a trench coat standing under a streetlight in a noir style.",
                "brand_id": brand.id,
                "key_tags": "Trendsetters, TechSavvy, BuzzWorthy",
                "audience_img": "SEED1A3.jpg",
            },
            {
                "name": "Active Boomers",
                "description": "Wellness-minded retirees enjoying nostalgia and classic comedy. “Classic Whodunit, Modern Twist” pairs Steve Martin, Martin Short, and gentle mysteries for engaging fun.",
                "psycho_graphic": "Emphasize active living, wellness, and staying engaged in retirement. Spend on health products, travel, and leisure experiences.",
                "attitudinal": "I focus on staying healthy, active, and independent as I age. I want products and services that help me live my best life with ease and balance. I value simple, practical solutions that enhance my wellness and lifestyle.",
                "self_concept": "I see myself as vibrant, youthful, and ready to enjoy life to its fullest.",
                "lifestyle": "Focused on health, wellness, and active living.",
                "media_habits": "Morning talk shows, daytime TV, news, and golf or baseball sports programming.",
                "general_keywords": "Active retirement, Senior wellness, Healthy aging, Financial security, Fitness for seniors, Healthcare solutions, Travel and leisure, Lifestyle balance, Suburban comfort, Nutrition and supplements.",
                "brand_keywords": "Steve Martin and Martin Short nostalgia, Light-hearted crime-solving, Classic comedic charm, Active aging and wit, Wholesome TV fun, Throwback humor meets modern twist, Old-school meets new-school, Mystery without the gore, Iconic TV actors, New York apartment life.",
                "image_prompt": "A smartphone screen glowing brightly against a minimalistic background of social media icons.",
                "brand_id": brand.id,
                "key_tags": "Nostalgia, Wellness, Lighthearted Mystery",
                "audience_img": "SEED1A4.jpg",
            },
            {
                "name": "Strategic Sports Fans",
                "description": "Competitive enthusiasts who thrive on teamwork and excitement. “Solve the Play, Crack the Case” channels game-day spirit into comedic, interactive mystery-solving.",
                "psycho_graphic": "Highly passionate and emotionally invested in their favorite teams and sports. Spend on event tickets, merchandise, and subscriptions to live sports coverage.",
                "attitudinal": "I am deeply loyal to my favorite teams and enjoy sharing my passion with others. I thrive on the excitement of game day and the camaraderie it brings. I want access to the best sports content, merchandise, and experiences.",
                "self_concept": "I see myself as a spirited, team-oriented fan who values the thrill of competition.",
                "lifestyle": "Passionate about professional sports like the NFL, NBA, MLB, and college sports.",
                "media_habits": "Viewers of live sports broadcasts on networks like ESPN, Fox Sports, and NBC Sports.",
                "general_keywords": "Game day excitement, Fantasy leagues, Team loyalty, Live sports broadcasts, Jerseys and gear, Tailgating, Sports highlights, Major leagues (NFL, NBA, MLB), Fitness culture, Competitive spirit.",
                "brand_keywords": "Team up to solve the case, Mystery fans unite, Crime-solving as a game, Suspenseful team dynamics, Competition for clues, Victory of the underdogs, Fast-paced twists, Strategy and surprises, Podcast parallels (analysis like sports talk), Solving the final mystery 'play'.",
                "image_prompt": "A close-up of a smiling mask beside a small stage microphone.",
                "brand_id": brand.id,
                "key_tags": "Team Spirit, Competition, Mystery Play",
                "audience_img": "SEED1A5.jpg",
            },
            {
                "name": "Binge Lovers",
                "description": "These viewers indulge in their love for TV series, spending weekends catching up on their favorite Hulu shows, especially drawn towards gripping elements in OMITB.",
                "psycho_graphic": "Value experiences over possessions, prioritize representation in media",
                "attitudinal": "Open to innovation, driven by social justice",
                "self_concept": "View themselves as change-makers and advocates for inclusivity",
                "lifestyle": "Enjoy exploring new cultures, favor engaging and immersive experiences",
                "media_habits": "High engagement with TikTok and Instagram, favor short-form video content",
                "general_keywords": "Exploration, Authenticity, Inclusivity, Creativity, Technology, Community, Entertainment, Storytelling, Engagement, Diversity",
                "brand_keywords": "Engaging narratives, Relatable characters, Modern themes, Grounded in reality, Youthful perspective, Inclusive storytelling, Emotional connection, Social relevance, Trend-setting, High-quality production",
                "image_prompt": "A vibrant collage of digital streaming symbols and abstract youthful silhouettes.",
                "brand_id": brand.id,
                "key_tags": "Binge-watchers, Streaming Enthusiasts, Trendsetters",
                "audience_img": "SEED1A6.jpg",
            },
        ]

        demographics = [
            {
                "gender": "Both",
                "age_bracket": "25-54",
                "hhi": "75k-150k",
                "race": "Primarily Hispanic or Latino",
                "education": "High school diploma to some college",
                "location": "Urban centers like Los Angeles, Miami, Houston, and New York City",
            },
            {
                "gender": "Female",
                "age_bracket": "25-44",
                "hhi": "50k-75k",
                "race": "White and African American, skewed African American",
                "education": "High school diploma to some college",
                "location": "Suburban, small cities or rural areas",
            },
            {
                "gender": "Both",
                "age_bracket": "25-44",
                "hhi": "75k-150k",
                "race": "Diverse",
                "education": "College degree or higher",
                "location": "Urban areas such as New York, Chicago, Los Angeles, and Austin",
            },
            {
                "gender": "Male",
                "age_bracket": "65+",
                "hhi": "150k-250k",
                "race": "Primarily White, with growing representation of all other ethnicities",
                "education": "High school diploma to college degree",
                "location": "Suburban",
            },
            {
                "gender": "Predominantly male, with growing female engagement",
                "age_bracket": "18-45",
                "hhi": "75k-150k",
                "race": "Diverse",
                "education": "High school diploma to some college or bachelor’s degree",
                "location": "Urban and suburban",
            },
            {
                "gender": "Both",
                "age_bracket": "35-54",
                "hhi": ">250k",
                "race": "Predominantly White",
                "education": "Bachelor’s degree or higher",
                "location": "Affluent suburbs and urban centers",
            },
        ]

        triggers = [
            [
                {
                    "name": "Familia Fiesta Mystery Night",
                    "description": "Gather the family for a bilingual mystery filled with humor, heartfelt moments, and unforgettable characters. 'Only Murders in the Building' is the perfect show to bond over, with a touch of telenovela drama and light-hearted suspense.",
                    "territory": "Mystery",
                    "trigger_img": "SEED1A1T1.jpg",
                },
                {
                    "name": "Movie Night Under the Stars",
                    "description": "Hosting a movie night with loved ones can evoke nostalgia and create lasting memories, especially in Latin households. This trigger encourages families to choose Hulu for their viewing pleasure, emphasizing the platform's vast library of films and series that cater to cultural interests. The excitement of sharing stories and laughter during these nights solidifies the need for an ongoing subscription.",
                    "territory": "Star Power",
                    "trigger_img": "SEED1A1T2.jpg",
                },
                {
                    "name": "Milestone Celebrations",
                    "description": "Key personal milestones such as birthdays, anniversaries, or graduations are cherished in Hispanic families. These events often serve as opportunities for gathering and reflecting on shared milestones, where Hulu’s relatable content can enhance the celebratory atmosphere. By showcasing exclusive content catering to these occasions, families are motivated to retain their subscriptions and explore new offerings for future events.",
                    "territory": "Milestone Celebrations",
                    "trigger_img": "SEED1A1T3.jpg",
                },
            ],
            [
                {
                    "name": "Mystery Night Without the Splurge",
                    "description": "Affordable, wholesome entertainment for the whole family. Dive into a quirky mystery series that’s perfect for cozy nights at home—no expensive tickets or subscriptions required.",
                    "territory": "Mystery",
                    "trigger_img": "SEED1A2T1.jpg",
                },
                {
                    "name": "Seasonal Series Binge-Watch",
                    "description": "The onset of a new season prompts viewers to seek fresh and exciting content. As cooler temperatures invite people indoors, they turn to Hulu for series that captivate their interest and provide escape. This is the perfect time for subscribers to dive into compelling stories and notable characters, enhancing their viewing experience and fostering emotional connections with the content.",
                    "territory": "Star Power",
                    "trigger_img": "SEED1A2T2.jpg",
                },
                {
                    "name": "New Year, New Beginnings",
                    "description": "As the new year approaches, many individuals reflect on personal growth and new resolutions. Subscriptions to Hulu become not just an entertainment choice but a partner in achieving personal aspirations like self-care or family time. With Fresh starts in mind, Hulu offers a diverse selection of uplifting content to inspire and motivate viewers to kick off their year positively and purposefully.",
                    "territory": "New Beginnings",
                    "trigger_img": "SEED1A2T3.jpg",
                },
            ],
            [
                {
                    "name": "Binge-Worthy Whodunit",
                    "description": "Join the cultural conversation! 'Only Murders in the Building' delivers stylish mysteries, modern twists, and Selena Gomez’s iconic performance—perfect for your next binge-watch session.",
                    "territory": "True Crime Podcast",
                    "trigger_img": "SEED1A3T1.jpg",
                },
                {
                    "name": "Cozy Evenings",
                    "description": "As the weather turns colder, trendy millennials look for activities that allow them to unwind after a busy week. The desire for comfort and relaxation during the fall and winter months evokes a need for cozy nights in and binge-watching sessions with friends. Hulu can be their go-to source for captivating series and movies that enhance these moments, transforming their evenings into memorable experiences filled with shared laughter and suspense.",
                    "territory": "The Building",
                    "trigger_img": "SEED1A3T2.jpg",
                },
                {
                    "name": "Milestone Celebrations",
                    "description": "Young millennials often celebrate significant milestones, such as moving into their first apartments or landing their dream jobs. These events inspire them to seek out entertainment options that elevate their celebratory moments. Hulu presents itself as a perfect companion for parties and gatherings, featuring content that resonates with their unique experiences and stories of success, making the platform a staple for social events.",
                    "territory": "Star Power",
                    "trigger_img": "SEED1A3T3.jpg",
                },
            ],
            [
                {
                    "name": "Classic Whodunit, Modern Twist",
                    "description": "Rediscover the joy of TV with Steve Martin and Martin Short’s classic comedic charm. 'Only Murders in the Building' offers a clever, lighthearted mystery with a modern twist—perfect for active minds and nostalgic hearts.",
                    "territory": "Star Power",
                    "trigger_img": "SEED1A4T1.jpg",
                },
                {
                    "name": "Celebration of Milestones",
                    "description": "Milestones such as anniversaries or birthdays prompt Boomers to seek entertainment for gatherings. They value shared experiences, especially when celebrating with loved ones, and lean toward options that provide engaging content suitable for all ages. This trigger encourages them to retain their Hulu subscriptions as it promises a network of diverse programming, creating memorable moments in their lives while ensuring laughter and joy with family and friends.",
                    "territory": "The Building",
                    "trigger_img": "SEED1A4T2.jpg",
                },
                {
                    "name": "Seasonal Cozy Comedies",
                    "description": "As seasons change, Boomers desire warm, comforting experiences in their downtime. Facing the chill of winter or the occasional rainy day, they seek light-hearted comedies that evoke laughter and joy, providing an escape from daily stresses. This seasonal shift motivates them to minimize churn by finding solace in Hulu’s engaging content, ensuring that their favorite shows are always just a click away during cozy indoor moments.",
                    "territory": "Mystery",
                    "trigger_img": "SEED1A4T3.jpg",
                },
            ],
            [
                {
                    "name": "Solve the Play, Crack the Case",
                    "description": "Love strategy and competition? Team up with Steve Martin, Martin Short, and Selena Gomez as they unravel a thrilling whodunit packed with twists, turns, and plenty of laughs.",
                    "territory": "Mystery",
                    "trigger_img": "SEED1A5T1.jpg",
                },
                {
                    "name": "Milestone Moments",
                    "description": "Celebrating personal milestones such as graduations, engagements, or promotions prompts a desire for risk-free entertainment that can galvanize shared experiences. By positioning Hulu's library of feel-good films and series around these events, it encourages current customers to retain subscriptions to create memorable moments with loved ones.",
                    "territory": "True Crime Podcast",
                    "trigger_img": "SEED1A5T2.jpg",
                },
                {
                    "name": "Seasonal Significance",
                    "description": "The arrival of different seasons triggers specific viewing habits; for instance, the cozy, introspective mood of autumn inspires binge-watching of beloved series and movies. By promoting themed collections on Hulu that align with the fall season, current subscribers can rediscover content that resonates with their emotional state, aiding in minimizing churn.",
                    "territory": "Star Power",
                    "trigger_img": "SEED1A5T3.jpg",
                },
            ],
            [
                {
                    "name": "The Art of the Whodunit",
                    "description": "Step into the world of high-end New York apartments and exclusive mysteries. 'Only Murders in the Building' combines elite wit, luxury living, and a sophisticated yet quirky storyline—perfect for discerning tastes.",
                    "territory": "Mystery",
                    "trigger_img": "SEED1A6T1.jpg",
                },
                {
                    "name": "Comfort During Life Changes",
                    "description": "During significant life changes, such as moving to a new city or navigating a career transition, people often seek solace in familiar, engaging content. Hulu serves as an emotional refuge, offering viewers a way to unwind and escape from stress during these transitions. By providing supportive and entertaining series that resonate with their experiences, Hulu becomes an essential part of their journey, encouraging continued subscriptions.",
                    "territory": "The Building",
                    "trigger_img": "SEED1A6T2.jpg",
                },
                {
                    "name": "Exclusive Event Celebration",
                    "description": "Celebrate personal milestones such as birthdays or promotions with a dedicated streaming night featuring Hulu's latest content. Users often seek unique experiences to enhance their special moments, and Hulu can provide exclusive access to vibrant new releases and series. The emotional connection tied to these life events fosters a sense of celebration and togetherness, driving subscriptions to elevate their entertainment choices.",
                    "territory": "Milestone Celebrations",
                    "trigger_img": "SEED1A6T3.jpg",
                },
            ],
        ]

        for audience_data, demographic_data, trigger_list in zip(
            audiences, demographics, triggers
        ):
            audience = Audience.objects.create(**audience_data)
            demographics = Demographics.objects.create(
                audience=audience, **demographic_data
            )
            for trigger_data in trigger_list:
                trigger = Trigger.objects.create(audience=audience, **trigger_data)

        brand.brand_summary_active = True
        brand.strategic_goals_active = True
        brand.audience_active = True
        brand.brand_universe_active = True
        brand.ad_legacy_active = True

        brand.save()
        brand_info.save()
        strategic_goal.save()
        audience.save()
        demographics.save()
        trigger.save()

        print(f"Brand created for user {user.username}.")

    else:
        print(f"Brand already exists for user {user.username}.")
