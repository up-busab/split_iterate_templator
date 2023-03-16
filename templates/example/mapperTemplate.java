public class [[VMType]]Mapper extends BaseMapper<[[VOType]],[[VMType]]> {

    @Override
    public [[VMType]] map([[VOType]] vo) {
		if (vo == null) {
			return null;
		} else {
			[[VMType]] entity = new [[VMType]]();
/*<SPLIT>*/		
/*<ITERATE>(property,'')*/
			entity.set[[property.name]](map[[property.name]](vo));
/*<SPLIT>*/
			return entity;
		}
    }

/*<SPLIT>*/
/*<ITERATE>(property,'')*/	
    private DataElement<[[property.type]]> map[[property.name]]([[VOType]] vo) {
        return getDataElementFactory().createSecureDataElement(vo.get[[property.name]](), DEFAULT_INSTRUCTION);
    }
/*<SPLIT>*/	
}