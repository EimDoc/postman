
def create_donor_text(donors):
    base = "Список каналов-доноров:\n"
    for i, donor in enumerate(donors):
        base += f"{i+1}. <b>{donor[2]}: {donor[1]}</b>\n"

    return base


def create_receiver_text(donors):
    base = "Список каналов-получателей:\n"
    for i, donor in enumerate(donors):
        base += f"{i+1}. <b>{donor[2]}: {donor[1]}</b>\n"

    return base


def create_tags_text(tags):
    base = "Список тегов:\n"
    for tag in tags:
        base += f"- <b>{tag[1]}</b>\n"

    return base
