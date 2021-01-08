import os
import pandas as pd

import backend


def main():
    """
    Function main that execute the program
    :return:
    """
    loop = True
    while loop:
        backend.print_menu()
        choice = backend.handle_choice_menu(4)

        if choice == 1:
            backend.try_download_file()

        elif choice == 2:
            done = False
            while not done:
                try:
                    national_data = pd.read_json("data" + os.sep + "national.json")
                    backend.print_submenu2()
                    variable = national_data.columns[::]
                    variable = variable.delete([0, 1, 11, 12, 16, 18, 19])
                    choice = backend.handle_choice_menu()
                except ValueError:
                    print("[i] File not found but I am gonna do it for you!\n")
                    backend.try_download_file()
                    national_data = pd.read_json("data" + os.sep + "national.json")
                    backend.print_submenu2()
                    variable = national_data.columns[::]
                    variable = variable.delete([0, 1, 11, 12, 16, 18, 19])
                    choice = backend.handle_choice_menu()

                if choice == 1:
                    backend.national_mean_7_days("data" + os.sep + "national.json")

                elif choice == 2:
                    backend.time_series("data" + os.sep + "national.json")

                elif choice == 3:
                    backend.max_min("data" + os.sep + "national.json")

                elif choice == 4:
                    national_data["data"] = national_data["data"].str[0:10]
                    backend.quotient_variable(national_data)

                elif choice == 5:
                    print("[i] Going back to Main Menu")
                    done = True
                    break

                else:
                    print("[i] Invalid assignment, please pay attention")

        elif choice == 3:
            done = False
            while not done:
                try:
                    regional_data = pd.read_json("data" + os.sep + "regional.json")
                    backend.print_submenu3()
                    choice = backend.handle_choice_menu(3)
                except ValueError:
                    print("[i] File not found but I am gonna do it for you!\n")
                    regional_data = pd.read_json("data" + os.sep + "regional.json")
                    backend.try_download_file()
                    backend.print_submenu3()
                    choice = backend.handle_choice_menu(3)

                if choice == 1:
                    backend.temporary_graph(regional_data)

                elif choice == 2:
                    backend.geographic_graph(regional_data)

                elif choice == 3:
                    print("[i] Going back to Main Menu")
                    done = True
                    break


                else:
                    print("[i] Invalid assignment, please pay attention")

        elif choice == 4:
            backend.show_credits()

        elif (choice.lower())[0]=='e':
            print("[i] Bye bye! See you soon.")
            break

        else:
            print("[i] Invalid assignment, please pay attention")


if __name__ == '__main__':
    main()
