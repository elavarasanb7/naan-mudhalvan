from dotenv import load_dotenv
import os
from supabase import create_client

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

# Supply chain management knowledge base
knowledge_base = {
    'inventory': {
        'keywords': ['inventory', 'stock', 'storage', 'warehouse'],
        'responses': [
            "Based on current inventory levels, I recommend optimizing stock levels to reduce holding costs while maintaining service levels.",
            "Our warehouse management system shows real-time inventory tracking and automated reordering capabilities.",
            "I can help you implement ABC analysis for better inventory control and management.",
            "Let's analyze your inventory turnover ratio to identify slow-moving items and optimize storage space.",
            "I can help set up automated reorder points based on lead times and demand patterns."
        ]
    },
    'logistics': {
        'keywords': ['shipping', 'transport', 'delivery', 'logistics', 'route', 'distribution'],
        'responses': [
            "Our logistics network optimization suggests using multi-modal transportation to reduce costs and delivery times.",
            "I can help track shipments and provide real-time updates on delivery status.",
            "Based on current data, I recommend optimizing delivery routes to improve efficiency.",
            "Let's analyze your last-mile delivery performance and identify areas for improvement.",
            "I can help implement cross-docking strategies to reduce warehouse handling time."
        ]
    },
    'procurement': {
        'keywords': ['supplier', 'vendor', 'purchase', 'procurement', 'buy', 'sourcing'],
        'responses': [
            "I can help evaluate supplier performance metrics and suggest improvements.",
            "Our system shows multiple vendor options for your requirements with comparative analysis.",
            "Based on market analysis, now is an optimal time to negotiate new supplier contracts.",
            "Let's implement a strategic sourcing approach to diversify your supplier base.",
            "I can help develop a vendor rating system based on quality, delivery, and cost metrics."
        ]
    },
    'forecasting': {
        'keywords': ['forecast', 'demand', 'predict', 'planning', 'projection'],
        'responses': [
            "Using historical data and market trends, I predict a 15% increase in demand for next quarter.",
            "I can help create a demand forecast using multiple forecasting methods for better accuracy.",
            "Our predictive analytics suggest adjusting safety stock levels for seasonal variations.",
            "Let's implement machine learning models for more accurate demand predictions.",
            "I can help analyze external factors affecting demand patterns in your market."
        ]
    },
    'quality_control': {
        'keywords': ['quality', 'inspection', 'standards', 'compliance', 'testing', 'defect'],
        'responses': [
            "I can help implement a comprehensive quality management system across your supply chain.",
            "Let's set up automated quality inspection checkpoints at key stages of the process.",
            "Based on recent data, I recommend implementing Six Sigma methodologies to reduce defects.",
            "Our analysis shows opportunities to improve supplier quality compliance.",
            "I can help develop quality metrics and KPIs for better monitoring and control."
        ]
    },
    'sustainability': {
        'keywords': ['sustainable', 'green', 'environmental', 'carbon', 'recycling', 'emissions'],
        'responses': [
            "Let's analyze your supply chain's carbon footprint and identify reduction opportunities.",
            "I can help implement sustainable packaging solutions to reduce environmental impact.",
            "Our assessment shows potential for implementing circular economy practices in your operations.",
            "I can help develop a sustainability scorecard for your suppliers.",
            "Let's explore renewable energy options for your warehousing operations."
        ]
    },
    'risk_management': {
        'keywords': ['risk', 'disruption', 'contingency', 'backup', 'emergency', 'resilience'],
        'responses': [
            "I can help develop comprehensive risk mitigation strategies for your supply chain.",
            "Let's create contingency plans for potential supply chain disruptions.",
            "Based on market analysis, I recommend diversifying your supplier base to reduce risks.",
            "Our system can simulate various risk scenarios to test supply chain resilience.",
            "I can help implement real-time risk monitoring and alert systems."
        ]
    },
    'cost_optimization': {
        'keywords': ['cost', 'expense', 'savings', 'efficiency', 'budget', 'optimization'],
        'responses': [
            "Our analysis shows potential cost savings through improved inventory management.",
            "I can help identify and eliminate non-value-adding activities in your supply chain.",
            "Let's analyze transportation costs and suggest optimization strategies.",
            "Our system can help optimize warehouse layout for improved operational efficiency.",
            "I can help implement activity-based costing for better cost control."
        ]
    },
    'technology_integration': {
        'keywords': ['technology', 'automation', 'digital', 'software', 'system', 'integration'],
        'responses': [
            "I can help evaluate and implement suitable supply chain management software solutions.",
            "Let's explore automation opportunities in your warehouse operations.",
            "Our analysis suggests implementing IoT sensors for better inventory tracking.",
            "I can help develop a roadmap for digital transformation of your supply chain.",
            "Let's integrate blockchain technology for better supply chain transparency."
        ]
    }
}

def populate_knowledge_base():
    try:
        # Insert new data
        for category, data in knowledge_base.items():
            # Check if category already exists
            existing = supabase.table('knowledge_base').select('*').eq('category', category).execute()
            
            if existing.data:
                # Update existing category
                supabase.table('knowledge_base')\
                    .update({
                        'keywords': data['keywords'],
                        'responses': data['responses']
                    })\
                    .eq('category', category)\
                    .execute()
                print(f"✅ Updated category: {category}")
            else:
                # Insert new category
                supabase.table('knowledge_base').insert({
                    'category': category,
                    'keywords': data['keywords'],
                    'responses': data['responses']
                }).execute()
                print(f"✅ Inserted new category: {category}")
        
        # Verify data
        response = supabase.table('knowledge_base').select('*').execute()
        print(f"✅ Verified {len(response.data)} categories in knowledge base")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    populate_knowledge_base() 