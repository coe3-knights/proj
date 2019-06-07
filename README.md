# pro_manager
This is the main repository for our COE 356 project.
<p> Group Name: <b>KNIGHTS</b> 
  <table><tr>
      <th colspan="3" >Members</th>
    </tr><tr>
      <th>Name</th> <th>Index No.</th> <th>Role</th>
    </tr><tr>
      <td>Attoh Attram Jonathan</td> <td></td> <td>Project Manager</td>
    </tr><tr>
      <td>Afeku Emmanuel</td> <td>5945516</td> <td>Frontend Lead</td>
    </tr><tr>
      <td>Nkrumah Adams Eugene</td> <td>5953416</td> <td>Frontend Support</td>
    </tr><tr>
      <td>Boakye Britwum Blessed</td> <td>5949416</td> <td>Backend Lead</td>
    </tr><tr>
      <td>Kreiger Godwin</td> <td>5952616</td> <td>Backend Support</td>
    </tr><tr>
      <td>Quansah Anthony Kwame Jacklingo</td> <td>5955416</td> <td>Backend Support</td>
    </tr><tr>
      <td>Adu Akoh Ernest</td> <td>5945216</td> <td>Chief Analyst</td>
    </tr>
  </table>
</p>
<p> Please review and make the necessary edits to the table.</p>

<hr>

Please follow these steps to set-up your system for this project.

1. Open up your terminal and run this code

    #### `git clone https://github.com/coe3-knights/pro_manager`

2. Open the server directory and open a new terminal or run 
    #### `cd pro_manager/server`

3. Create a virtual environment with the code below
    #### `python3 -m venv venv`

4. Activate the virtual environment
    #### `source venv/bin/activate`
    You terminal should now have the prompt
        `(venv) user@machine:~/my_relative_path/pro_manager/server$`

5. Upgrade pip to avoid the build-wheel error when you perform the next step. Run
    #### `pip install -U pip`

6. Install all the dependecies listed in the requirements.txt file. Run
    #### `pip install -r reqiurements.txt`
    
7. Create the sqlite db file by running 
    #### `flask db upgrade`

8. Open the project folder in your favorite editor and have fun coding.
