from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import (
    Brand,
    BrandInfo,
    AdvertisingLegacy,
    Audience,
    StrategicGoals,
    Trigger,
    Demographics,
)
from django.utils import timezone


class Command(BaseCommand):
    help = "Populate the database with Only Murders In The Building brand data."

    def handle(self, *args, **kwargs):
        users = User.objects.all()

        if not users.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Nenhum usuário encontrado. Crie usuários antes de rodar este seed."
                )
            )
            return

        for user in users:
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
                    strategic_goal = StrategicGoals.objects.create(
                        brand_id=brand, goal=goal
                    )

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
                    },
                ]

                for audience in audiences:
                    audience = Audience.objects.create(**audience)

                demographics = Demographics.objects.create(
                    audience=audience,
                    gender=["Male", "Female", "Non-binary"],
                    age_bracket="25-34",
                    hhi="75k-100k",
                    race=["Caucasian", "Hispanic", "African-American"],
                    education="Superior completo ou acima",
                    location="Grandes cidades e metrópoles.",
                )

                # Criando Trigger
                trigger = Trigger.objects.create(
                    audience=audience,
                    name="Assassinato no Arconia",
                    description="Um crime misterioso acontece no prédio e precisa ser investigado.",
                    territory="Narrativas de mistério, ficção criminal.",
                )

                brand.brand_summary_active = True
                brand.strategic_goals_active = True
                brand.audience_active = True

                brand.save()
                brand_info.save()
                strategic_goal.save()
                audience.save()
                demographics.save()
                trigger.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Brand {brand.name} created successfully for user {user.username}."
                    )
                )

            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"The user {user.username} already has a brand created."
                    )
                )

        self.stdout.write(self.style.SUCCESS("Seed executado com sucesso!"))
