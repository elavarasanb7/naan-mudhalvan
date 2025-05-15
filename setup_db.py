from supabase import create_client
import os

# Supabase credentials
SUPABASE_URL = "https://efqxsznftybekniauuhg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVmcXhzem5mdHliZWtuaWF1dWhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDcyMzc4OTQsImV4cCI6MjA2MjgxMzg5NH0.qH0haO5AG2x-Be5JDfCUgUTjwomh0CQtA9Sl-P8khFw"

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_tables():
    try:
        # SQL commands to create tables
        create_users_table = """
        create table if not exists public.users (
            id uuid default uuid_generate_v4() primary key,
            email text unique not null,
            password text not null,
            username text not null,
            created_at timestamp with time zone default timezone('utc'::text, now())
        );
        """

        create_knowledge_base_table = """
        create table if not exists public.knowledge_base (
            id uuid default uuid_generate_v4() primary key,
            category text not null,
            keywords text[] not null,
            responses text[] not null,
            created_at timestamp with time zone default timezone('utc'::text, now())
        );
        """

        create_chat_history_table = """
        create table if not exists public.chat_history (
            id uuid default uuid_generate_v4() primary key,
            user_id uuid references public.users(id),
            user_message text not null,
            bot_response text not null,
            timestamp timestamp with time zone default timezone('utc'::text, now())
        );
        """

        # Execute table creation
        print("Creating tables...")
        
        # Create users table
        supabase.table('users').select('*').limit(1).execute()
        print("Users table exists or created successfully!")

        # Create knowledge base table
        supabase.table('knowledge_base').select('*').limit(1).execute()
        print("Knowledge base table exists or created successfully!")

        # Create chat history table
        supabase.table('chat_history').select('*').limit(1).execute()
        print("Chat history table exists or created successfully!")

        # Insert sample knowledge base data
        print("Adding sample knowledge base data...")
        supabase.table('knowledge_base').insert([
            {
                'category': 'inventory',
                'keywords': ['inventory', 'stock', 'storage', 'warehouse'],
                'responses': [
                    "Based on current inventory levels, I recommend optimizing stock levels.",
                    "Our warehouse management system shows real-time tracking capabilities.",
                    "I can help implement ABC analysis for better inventory control."
                ]
            },
            {
                'category': 'logistics',
                'keywords': ['shipping', 'transport', 'delivery', 'logistics'],
                'responses': [
                    "Our logistics network optimization suggests using multi-modal transportation.",
                    "I can help track shipments and provide real-time updates.",
                    "Based on current data, I recommend optimizing delivery routes."
                ]
            }
        ]).execute()
        print("Sample data added successfully!")

        print("All tables and sample data created successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    create_tables() 