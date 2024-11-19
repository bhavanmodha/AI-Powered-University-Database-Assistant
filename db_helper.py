import pandas as pd

def get_marks(params):
    student_name = params.get('student_name', '')
    semester = params.get('semester', '')
    operation = params.get('operation', '')
    if semester is None:
        raise ValueError("Semester must be specified.")
    

    marks_df = pd.read_csv("./db/marks.csv")
    filtered_df = marks_df[marks_df['semester'] == semester]
    
    result = None
    if student_name:
        # Filter for the specific student
        student_gpa = filtered_df[filtered_df['student_name'].str.lower() == student_name.lower()]
        if not student_gpa.empty:
            result = student_gpa.iloc[0]['gpa']
        else:
            result = -1  
    elif operation == 'max':
        result = filtered_df['gpa'].max()
    elif operation == 'min':
        result = filtered_df['gpa'].min()
    elif operation == 'avg':
        result = filtered_df['gpa'].mean()
    else:
        raise ValueError("Invalid operation specified. Use 'max', 'min', or 'avg'.")
    
    # Handle case when result is None or NaN (no matching records)
    if pd.isnull(result):
        result = -1

    return round(result, 2) if result != -1 else result

def get_fees(params):
    student_name = params.get('student_name', '')
    semester = params.get('semester', '')
    fees_type = params.get('fees_type', '')
    
    if semester is None:
        raise ValueError("Semester must be specified.")
    if fees_type not in ['paid', 'pending', 'total']:
        raise ValueError("fees_type must be 'paid', 'pending', or 'total'.")
    
    fees_df = pd.read_csv("./db/fees.csv")

    filtered_df = fees_df[fees_df['semester'] == semester]
    
    result = None
    
    if student_name:
        student_fees = filtered_df[filtered_df['student_name'].str.lower() == student_name.lower()]
        if not student_fees.empty:
            if fees_type == 'paid':
                result = student_fees.iloc[0]['paid']
            elif fees_type == 'pending':
                result = student_fees.iloc[0]['pending']
            elif fees_type == 'total':
                result = student_fees.iloc[0]['total_fees']
        else:
            result = -1  # No records found for the student
    else:
        # Aggregate data for the entire semester if no student_name is provided
        if fees_type == 'paid':
            result = filtered_df['paid'].sum()
        elif fees_type == 'pending':
            result = filtered_df['pending'].sum()
        elif fees_type == 'total':
            result = filtered_df['total_fees'].sum()
    
    # Handle case when result is None or NaN (no matching records)
    if pd.isnull(result):
        result = -1

    return int(result) if result != -1 else result


# if __name__ == "__main__":
#     print(get_marks({
#         'semester': 4,
#         'operation': 'max'
#     }))


#     print(get_fees({
#         'student_name': "Peter Pandey",
#         'semester': 1,
#         'fees_type': 'paid'
#     }))


    