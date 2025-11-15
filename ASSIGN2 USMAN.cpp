#include <iostream>
#include <string>
using namespace std;

/*
    "TechSolutions Employee Management System"

    . Manages employee personal data, salary, and performance
    . Demonstrates OOP concepts: constructors, copy constructors,
      deep copy vs shallow copy, const/static members, and object handling
    Author: [USMAN IQBAL]
    Date  : [15-11-2025]
*/

class Employee {
private:
    string* name;                
    int id;
    float salary;
    float performance;          

    static int count;           
    static const string companyName;

public:
  
    Employee(const string& n, int id, float salary, float performance = 0.0f)
        : id(id), salary(salary), performance(performance) {
        this->name = new string(n);
        count++;  
    }

    Employee(const Employee& other)
        : id(other.id), salary(other.salary), performance(other.performance) {
        name = new string(*(other.name)); 
        count++;
        cout << "[Deep Copy Constructor Called for " << *name << "]\n";
    }

    Employee(Employee* other, bool shallow) {
        id = other->id;
        salary = other->salary;
        performance = other->performance;
        name = other->name; 
        count++;
        cout << "[Shallow Copy Constructor Called for " << *name << "]\n";
    }

    ~Employee() {
        delete name;
    }

    void setSalary(float salary) {
        this->salary = salary;
    }

    void setPerformance(float perf) {
        performance = perf;
    }

    void changeName(const string& newName) {
        delete name;
        name = new string(newName);
    }

    void display() const {
        cout << "Company: " << companyName << endl;
        cout << "ID      : " << id << endl;
        cout << "Name    : " << *name << endl;
        cout << "Salary  : " << salary << endl;
        cout << "Performance: " << performance << endl;
       
    }

    void compareSalary(const Employee& other) const {
        if (salary > other.salary)
            cout << *name << " has a higher salary than " << *(other.name) << ".\n";
        else if (salary < other.salary)
            cout << *name << " has a lower salary than " << *(other.name) << ".\n";
        else
            cout << *name << " and " << *(other.name) << " have equal salaries.\n";
    }

    Employee getBonusEmployee(float bonus) const {
        Employee temp(*name, id, salary + bonus, performance);
        return temp;
    }

    static void showTotalEmployees() {
        cout << "Total employees currently: " << count << endl;
    }
};

int Employee::count = 0;
const string Employee::companyName = "TechSolutions";

int main() {
    cout << "TechSolutions Employee Management System\n";

    Employee* e1 = new Employee("zamad", 101, 50000, 7.5);
    cout << "Employee 1 :\n";
    e1->display();

    Employee e2("zaman", 102, 60000, 8.5);
    cout << "Employee 2:\n";
    e2.display();

    cout << "Comparing Salaries:\n";
    e1->compareSalary(e2);
    
    Employee e3 = e2.getBonusEmployee(5000);
    cout << "After bonus\n";
    cout << "Employee 3:\n";
    e3.display();

    Employee::showTotalEmployees();
    cout << endl;

    cout << "Deep Copy Demonstration\n";
    
    Employee deepOriginal("usman", 201, 70000, 9.0);
    Employee deepCopy(deepOriginal);

    cout << "Before changing original:\n";
    deepOriginal.display();
    cout << "The copy is as follow:\n";
    deepCopy.display();

    deepOriginal.changeName("usman iqbal");
    deepOriginal.setPerformance(9.5);
    cout << "After changing original:\n";
    deepOriginal.display();
    cout << "The effect on the copy is as follow:\n";
    deepCopy.display();
    cout << endl;

    cout << "Shallow Copy Demonstration\n";
    Employee shallowOriginal("ahmad", 301, 80000, 8.0);
    cout << "Original:\n";
    shallowOriginal.display();

    Employee shallowCopy(&shallowOriginal, true); 

    cout << "Shallow Copy after assignment:\n";
    shallowCopy.display();

    shallowOriginal.changeName("ahmad razza");
    shallowOriginal.setPerformance(8.5);

    cout << "After changing original:\n";
    shallowOriginal.display();
    cout << "Effect on shallow copy:\n";
    shallowOriginal.display();

    delete e1;

    cout << endl;
    Employee::showTotalEmployees();
    system("pause");
    return 0;
}