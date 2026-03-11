from datetime import date
from db import setup_db, get_connection
from logger import generate_daily_log
from activity_creator import create_activity
from log_editor import edit_today_log


# ------------------------
# Display today's activities
# ------------------------
def show_today(return_rows = False):
    today = date.today().isoformat()
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(
    '''
        SELECT  d.id, a.name, d.completed, d.duration, d.quantity, d.satisfaction
        FROM daily_logs d
        JOIN activities a ON d.activity_id = a.id
        WHERE d.date = ?
        ORDER BY a.name
    ''', (today,))
    
    rows = cur.fetchall()
    conn.close()
    
    print(f"\nActivity Log for {today}\n")
    
    if not rows:
        print("No activities scheduled for today.")
        return [] if return_rows else None
    
    for i, r in enumerate(rows, 1):
        status = "✔" if r[2] else "☐"
        print(f"{i}. {status} {r[1]}")
        
    if return_rows:
        return rows
    
    
# ------------------------
# Toggle completion checkbox
# ------------------------
def mark_completed():
    rows = show_today(return_rows=True)

    if not rows:
        print("No activities scheduled for today.")
        return
    
    choice = input("\nEnter activity number to toggle completion (or 'q' to cancel): ").strip()
    
    if choice == "q":
        return
    
    if not choice.isdigit():
        print("❌ Invalid input.")
        return
    
    index = int(choice) - 1
    if index < 0 or index >= len(rows):
        print("❌ Invalid activity number.")
        return
    
    log_id, name, completed, duration, quantity, satisfaction = rows[index]
    new_status = 0 if completed else 1
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
    '''
        UPDATE daily_logs
        SET completed = ?
        WHERE id = ?
    ''', (new_status, log_id))
    conn.commit()
    conn.close()
    
    print(f'✅ "{name}" marked as {"completed" if new_status else "incomplete"}.')
    


# ------------------------
# Edit activity details
# ------------------------
def edit_activity_details():
    rows = show_today(return_rows=True)

    if not rows:
        return

    choice = input("\nEnter activity number to edit details (or 'q' to cancel): ").strip()
    if choice == "q":
        return
    
    if not choice.isdigit():
        print("❌ Invalid input.")
        return
    
    index =int(choice) - 1
    if index < 0 or index >= len(rows):
        print("❌ Invalid activity number.")
        return
    
    log_id, name, completed, duration, quantity, satisfaction = rows[index]
    
    print(f"\nEditing {name}")
    
    new_duration = input(f"Duration [{duration or ''}]:").strip() or duration
    new_quantity = input(f"Quantity [{quantity or ''}]:").strip() or quantity

    new_satisfaction = satisfaction
    sat_input = input(f"Satisfaction (0–100) [{satisfaction if satisfaction is not None else ''}]:").strip()
    if sat_input:
        if sat_input.isdigit() and 0 <= int(sat_input) <= 100:
            new_satisfaction = int(sat_input)
        else:
            print("❌ Invalid satisfaction value. Keeping previous value.")
            return
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        '''
        UPDATE daily_logs
        SET duration = ?, quantity = ?, satisfaction = ?
        WHERE id = ?
        ''',
        (new_duration, new_quantity, new_satisfaction, log_id)
    )

    conn.commit()
    conn.close()

    print("✅ Activity details updated.")

# ------------------------
# Menu
# ------------------------
def menu():
    print("\n1. Create New Activity")
    print("2. Generate Today's Log")
    print("3. View Today's Log")
    print("4. Mark activity as completed")
    print("5. Edit activity details")
    print("6. Exit") 

# ------------------------
# Main loop
# ------------------------
if __name__ == "__main__":
    setup_db()
    generate_daily_log()
    show_today()
    mark_completed() 
                   
    while True:
        menu()
        choice = input("> ").strip()
        
        if choice == "1":
            create_activity()
            
        elif choice == "2":
            generate_daily_log()
            print("✅ Today's log generated.")
            
        elif choice == "3":
            show_today()
            
        elif choice == "4":
            mark_completed()
        
        elif choice == "5":
            edit_today_log()
            
        elif choice == "6":
            print("Goodbye 👋")
            break
        
        else:
            print("❌ Invalid option. Please choose 1–6.")
