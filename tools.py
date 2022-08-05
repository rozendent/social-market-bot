from data import db_session
from data.users import User, Association
from setup import texts, session


def make_user_message(user: User):
    res = f'''<b>Имя:</b> {user.name}
<b>Возраст:</b> {user.age}
<b>Сотрудничество онлайн/офлайн:</b> {texts["format_" + str(user.format)]} \n'''
    if user.city:
        res += f'<b>Город:</b> {user.city} \n'
    res += f'''<b>Сфера деятельности:</b> {user.get_str_spheres()}
<b>Специальность:</b> {user.role}

<b>Навыки:</b> 
{user.skills}

<b>Портфолио:</b> 
{user.achievements}

<b>Опыт конкурсной деятельности:</b> 
{user.experience}

<b>Требования к соучастнику:</b> 
{user.requirements}
'''
    return res


def get_relevant_user(msg_user_id: User):
    u = session.query(User).filter(User.user_id == msg_user_id).first()
    all = list(session.query(User).filter(User.user_id != u.user_id).all())
    all.sort(
        key=lambda x: (str(u.format) in str(x.format), str(u.city).lower() == str(x.city).lower, u.sphere == x.sphere))
    print(all)
    for user in all:
        a = session.query(Association).filter(Association.u1_id == msg_user_id,
                                              Association.u2_id == user.user_id).first()
        print(a)
        if a:
            pass
        else:
            a = Association(u1_id=msg_user_id, u2_id=user.user_id)
            session.add(a)
            session.commit()
            return user


def get_empty_spheres_dict():
    res = dict()
    for i in range(1, 16):
        res[i] = False
    return res


def get_list_from_spheres_dict(spheres_dict: dict):
    res = []
    for s in spheres_dict:
        if spheres_dict[s]:
            res.append(str(s))
    return str(', '.join(res))
