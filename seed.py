import sys
import os

# Add the current directory to sys.path to allow importing local modules
current_dir = os.path.dirname(os.path.realpath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from database import engine, SessionLocal
from models import Base, Category, Product

async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        # Create categories
        categories = [
            Category(name="Cycles", slug="cycles"),
            Category(name="Tyres", slug="tyres"),
            Category(name="Tech Services", slug="tech"),
            Category(name="Spare Parts", slug="spares"),
        ]
        db.add_all(categories)
        await db.commit()
        for c in categories:
            await db.refresh(c)

        cat_map = {c.slug: c.id for c in categories}

        # Sample Products
        products = [
            Product(
                name="PK Mountain Pro",
                slug="pk-mountain-pro",
                brand="PK Custom",
                description="The ultimate mountain companion. Crafted for rugged terrain with PK Mart precision engineering.",
                specs={"Frame": "Carbon Fiber", "Gears": "Shimano Deore 12-speed", "Suspension": "Fox Float 36"},
                price="₹45,000",
                image="/images/stories/apex_cycle.png",
                is_featured=1,
                category_id=cat_map["cycles"]
            ),
            Product(
                name="MRF Perfinza CLUX",
                slug="mrf-perfinza",
                brand="MRF",
                description="Unmatched comfort and high-speed stability. The Perfinza is designed for the luxury sedan experience.",
                specs={"Tread": "Asymmetric", "Compound": "Silica-based", "Warranty": "5 Years"},
                price="₹6,500",
                image="/images/stories/apex_tyre.png",
                is_featured=1,
                category_id=cat_map["tyres"]
            ),
            Product(
                name="CEAT SecuraDrive",
                slug="ceat-securadrive",
                brand="CEAT",
                description="Superior grip on wet and dry surfaces. Engineered for safety and longevity on Indian roads.",
                specs={"Type": "Radial", "Position": "Front/Rear", "Load Index": "91V"},
                price="₹5,800",
                image="/images/stories/apex_tyre.png",
                is_featured=0,
                category_id=cat_map["tyres"]
            ),
            Product(
                name="PK iPhone Precision Service",
                slug="pk-iphone-service",
                brand="PK Tech",
                description="Professional screen and battery replacement at PK Laptop & Mobile Service Center.",
                specs={"Service Time": "2 Hours", "Parts": "OEM Premium", "Warranty": "180 Days"},
                price="₹2,499",
                image="/images/stories/apex_tech.png",
                is_featured=1,
                category_id=cat_map["tech"]
            ),
            Product(
                name="PK Laptop Master Service",
                slug="pk-laptop-service",
                brand="PK Tech",
                description="Complete deep cleaning and performance optimization at the PK Tech Center.",
                specs={"Cleaning": "Ultrasonic", "Thermal Paste": "Kryonaut Extreme", "OS Opt": "Included"},
                price="₹1,200",
                image="/images/stories/apex_tech.png",
                is_featured=0,
                category_id=cat_map["tech"]
            ),
            Product(
                name="Shimano Deore Groupset",
                slug="shimano-deore",
                brand="Shimano",
                description="The gold standard for performance drivetrain systems. Reliable and smooth.",
                specs={"Speed": "12-speed", "Included": "Shifter, Derailleur, Chain, Cassette", "Weight": "1.8kg"},
                price="₹22,000",
                image="/images/stories/apex_spares.png",
                is_featured=0,
                category_id=cat_map["spares"]
            )
        ]
        db.add_all(products)
        await db.commit()

    print("PK Multiserve Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
