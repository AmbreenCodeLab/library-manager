import streamlit as st
import json
import os

# Set page configuration
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

# Initialize session state for library data
if 'library' not in st.session_state:
    st.session_state.library = []

# File handling functions
def load_library():
    if os.path.exists("library.books"):
        with open("library.books", "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open("library.books", 'w') as file:
        json.dump(library, file)

# Main title
st.title("📚 Library Management System")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["View Books", "Add Book", "Search Books", "Statistics"])

# Load library data
if not st.session_state.library:
    st.session_state.library = load_library()

if page == "Add Book":
    st.header("Add New Book")
    with st.form("add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.text_input("Year")
        genre = st.text_input("Genre")
        read = st.checkbox("Have you read this book?")
        
        if st.form_submit_button("Add Book"):
            new_book = {
                'title': title,
                'author': author,
                'year': year,
                'genre': genre,
                'read': read
            }
            st.session_state.library.append(new_book)
            save_library(st.session_state.library)
            st.success(f"Book '{title}' added successfully!")

elif page == "View Books":
    st.header("Library Collection")
    if not st.session_state.library:
        st.info("Your library is empty. Add some books!")
    else:
        for i, book in enumerate(st.session_state.library):
            with st.expander(f"{book['title']} by {book['author']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Year:** {book['year']}")
                with col2:
                    st.write(f"**Genre:** {book['genre']}")
                with col3:
                    st.write(f"**Status:** {'Read' if book['read'] else 'Unread'}")
                
                if st.button(f"Remove Book", key=f"remove_{i}"):
                    st.session_state.library.pop(i)
                    save_library(st.session_state.library)
                    st.success(f"Book '{book['title']}' removed successfully!")
                    st.rerun()

elif page == "Search Books":
    st.header("Search Books")
    search_type = st.selectbox("Search by", ["Title", "Author", "Genre"])
    search_term = st.text_input(f"Enter {search_type}").lower()
    
    if search_term:
        results = [book for book in st.session_state.library 
                  if search_term in book[search_type.lower()].lower()]
        if results:
            st.subheader("Search Results")
            for book in results:
                with st.expander(f"{book['title']} by {book['author']}"):
                    st.write(f"**Year:** {book['year']}")
                    st.write(f"**Genre:** {book['genre']}")
                    st.write(f"**Status:** {'Read' if book['read'] else 'Unread'}")
        else:
            st.info(f"No books found matching '{search_term}'")

elif page == "Statistics":
    st.header("Library Statistics")
    total_books = len(st.session_state.library)
    read_books = len([book for book in st.session_state.library if book['read']])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Books", total_books)
    with col2:
        st.metric("Read Books", read_books)
    with col3:
        percentage = (read_books / total_books * 100) if total_books > 0 else 0
        st.metric("Percentage Read", f"{percentage:.1f}%")
    
    # Genre distribution
    if st.session_state.library:
        st.subheader("Genre Distribution")
        genres = {}
        for book in st.session_state.library:
            genres[book['genre']] = genres.get(book['genre'], 0) + 1
        
        st.bar_chart(genres)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ by Rao-Ambreen") 